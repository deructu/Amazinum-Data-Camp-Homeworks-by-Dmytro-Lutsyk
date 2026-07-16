from pathlib import Path
import argparse
import json

import requests


def main():
    parser = argparse.ArgumentParser(description="Send a test image to the YOLO FastAPI server.")
    parser.add_argument("--image", default="sample_data/horse.jpeg", help="Path to input image")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="API base URL")
    parser.add_argument("--confidence", type=float, default=0.25, help="YOLO confidence threshold")
    args = parser.parse_args()

    image_path = Path(args.image)
    endpoint = f"{args.url.rstrip('/')}/detect"

    with image_path.open("rb") as image_file:
        response = requests.post(
            endpoint,
            params={"confidence": args.confidence},
            files={"image": (image_path.name, image_file, "image/jpeg")},
            timeout=60,
        )

    print("Status code:", response.status_code)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
