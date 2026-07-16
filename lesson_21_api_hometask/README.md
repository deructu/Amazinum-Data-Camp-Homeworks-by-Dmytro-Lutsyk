# Home task: API for Computer Vision

## Overview

This project implements a simple computer vision solution and deploys it as a FastAPI service.

The application accepts an input image, runs YOLO object detection, returns detected objects as JSON, and can also return an annotated image with bounding boxes.

## Deployment info

Chosen deployment format: **FastAPI Web API**.

The API is implemented in `app.py` and uses a local YOLO model file:

```text
models/yolo11n.pt
```

Sample data and examples are included in the folder, so the project can be checked locally.

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Modeling info

The model is YOLO, a real-time object detection model. It predicts:

- object class;
- confidence score;
- bounding box coordinates.

For this homework, the model is used in inference mode only. The weights are stored locally in `models/yolo11n.pt`.

## Interface description

### `GET /`

Checks that the API is running.

Output example:

```json
{
  "message": "YOLO Object Detection API is running",
  "docs": "/docs",
  "health": "/health"
}
```

### `GET /health`

Returns service status and model information.

Output fields:

- `status` - API status;
- `model_path` - path to local model weights;
- `model_exists` - whether model file exists;
- `classes_count` - number of YOLO classes.

### `POST /detect`

Runs object detection and returns JSON.

Input:

- multipart form file field named `image`;
- optional query parameter `confidence`, default `0.25`.

Output:

- input file name;
- input image shape;
- confidence threshold;
- detections count;
- list of detected objects;
- path to saved annotated image in `outputs/`.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/detect?confidence=0.25" ^
  -F "image=@sample_data/horse.jpeg"
```

### `POST /detect/image`

Runs object detection and returns an annotated JPG image directly.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/detect/image?confidence=0.25" ^
  -F "image=@sample_data/horse.jpeg" ^
  --output outputs/horse_detected.jpg
```

## Example process

Example request/response logs are saved in:

```text
examples/example_process_log.txt
examples/example_response.json
examples/api_process_screenshot.png
```

An example annotated image from the lesson demo is saved in:

```text
examples/processed_result_example.jpg
```

## Project structure

```text
lesson_21_api_hometask/
|-- app.py
|-- client_test.py
|-- requirements.txt
|-- README.md
|-- models/
|   `-- yolo11n.pt
|-- sample_data/
|   `-- horse.jpeg
|-- outputs/
`-- examples/
    |-- example_process_log.txt
    |-- example_response.json
    |-- api_process_screenshot.png
    `-- processed_result_example.jpg
```
