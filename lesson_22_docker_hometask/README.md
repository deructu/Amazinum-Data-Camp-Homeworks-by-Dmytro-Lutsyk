# Home task: Docker deployment for Computer Vision API

## Overview

This homework dockerizes a previous WebAPI computer vision solution.

The application is a FastAPI service that accepts an uploaded image, runs YOLO object detection, returns detected objects as JSON, and can return an annotated image with bounding boxes.

## Homework requirements covered

1. Docker deployment based on previous homework: `app.py` is a FastAPI YOLO object detection API.
2. `Dockerfile` is included.
3. `ENTRYPOINT` + `CMD` are configured through `docker-entrypoint.sh`, so different scripts can be executed by passing arguments to `docker run`.
4. Example commands and process logs are included in `examples/`.

## Project structure

```text
lesson_22_docker_hometask/
|-- app.py
|-- client_test.py
|-- smoke_check.py
|-- Dockerfile
|-- docker-entrypoint.sh
|-- docker-compose.yml
|-- requirements.txt
|-- README.md
|-- .dockerignore
|-- .gitignore
|-- models/
|   `-- yolo11n.pt
|-- sample_data/
|   `-- horse.jpeg
|-- outputs/
`-- examples/
    |-- commands_to_run.txt
    |-- example_docker_process_log.txt
    |-- example_detection_response.json
    `-- detected_horse_real.jpg
```

## Installation requirements

Install Docker Desktop and make sure Docker is running.

Check Docker:

```bash
docker --version
docker compose version
```

## Build Docker image

```bash
docker build -t lesson-22-docker-yolo-api .
```

## Run API container

```bash
docker run --rm -p 8000:8000 --name lesson_22_yolo_api lesson-22-docker-yolo-api
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## Run with Docker Compose

```bash
docker compose up --build
```

Stop services:

```bash
docker compose down
```

## Run scripts inside the container

The Dockerfile uses:

```dockerfile
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

This means that by default the container starts the API server.

But we can override the default command and run any script inside the image:

```bash
docker run --rm lesson-22-docker-yolo-api python smoke_check.py
```

Another example:

```bash
docker run --rm lesson-22-docker-yolo-api python -c "from app import MODEL_PATH; print(MODEL_PATH.exists())"
```

## Test API from host machine

Start the API container first, then run from the project folder:

```bash
python client_test.py --image sample_data/horse.jpeg
```

Expected result:

```text
Status code: 200
```

The API will save an annotated result image to:

```text
outputs/detected_horse.jpg
```

## Interface description

### `GET /`

Returns a basic API status message.

### `GET /health`

Returns model status and service information.

### `POST /detect`

Input:

- multipart field `image`;
- optional query parameter `confidence`, default `0.25`.

Output:

- filename;
- image shape;
- number of detections;
- detected object classes;
- confidence scores;
- bounding boxes;
- path to saved annotated image.

### `POST /detect/image`

Returns the annotated image directly as JPEG.

## Modeling info

The solution uses YOLO for object detection. The local model weights are stored in:

```text
models/yolo11n.pt
```

For the sample image `sample_data/horse.jpeg`, the model detects one object: `horse`.

## Example process

Command examples are saved in:

```text
examples/commands_to_run.txt
```

Example Docker logs are saved in:

```text
examples/example_docker_process_log.txt
```

Example API response is saved in:

```text
examples/example_detection_response.json
```
