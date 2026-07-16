from pathlib import Path
from typing import Any

import cv2
import io
import numpy as np
import uvicorn
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "yolo11n.pt"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Dockerized YOLO Object Detection API",
    description="FastAPI + YOLO computer vision service deployed with Docker.",
    version="1.0.0",
)

model = YOLO(str(MODEL_PATH))
class_names = model.names


def decode_image(contents: bytes) -> np.ndarray:
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")
    return image


def detect_objects(image: np.ndarray, confidence: float) -> tuple[Any, list[dict[str, Any]]]:
    result = model.predict(image, conf=confidence, verbose=False)[0]
    detections = []

    for box in result.boxes:
        class_id = int(box.cls[0])
        detections.append(
            {
                "class_id": class_id,
                "class_name": class_names[class_id],
                "confidence": round(float(box.conf[0]), 4),
                "bbox_xyxy": [round(float(value), 2) for value in box.xyxy[0].tolist()],
            }
        )

    return result, detections


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "Dockerized YOLO API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check() -> dict[str, Any]:
    return {
        "status": "ok",
        "model_path": str(MODEL_PATH.relative_to(BASE_DIR)),
        "model_exists": MODEL_PATH.exists(),
        "classes_count": len(class_names),
    }


@app.post("/detect")
async def detect(
    image: UploadFile = File(...),
    confidence: float = Query(0.25, ge=0.0, le=1.0),
) -> dict[str, Any]:
    contents = await image.read()
    input_image = decode_image(contents)
    result, detections = detect_objects(input_image, confidence)

    annotated_image = result.plot()
    output_name = f"detected_{Path(image.filename or 'uploaded.jpg').stem}.jpg"
    output_path = OUTPUT_DIR / output_name
    cv2.imwrite(str(output_path), annotated_image)

    return {
        "filename": image.filename,
        "image_shape": list(input_image.shape),
        "confidence_threshold": confidence,
        "detections_count": len(detections),
        "detections": detections,
        "annotated_image": str(output_path.relative_to(BASE_DIR)),
    }


@app.post("/detect/image")
async def detect_image(
    image: UploadFile = File(...),
    confidence: float = Query(0.25, ge=0.0, le=1.0),
) -> StreamingResponse:
    contents = await image.read()
    input_image = decode_image(contents)
    result, _ = detect_objects(input_image, confidence)

    annotated_image = result.plot()
    success, encoded_image = cv2.imencode(".jpg", annotated_image)
    if not success:
        raise HTTPException(status_code=500, detail="Could not encode result image")

    return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
