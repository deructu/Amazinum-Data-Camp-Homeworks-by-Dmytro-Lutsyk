from pathlib import Path

from app import MODEL_PATH, OUTPUT_DIR, app

print("Smoke check")
print("API title:", app.title)
print("Model exists:", MODEL_PATH.exists())
print("Output directory exists:", OUTPUT_DIR.exists())
print("Available routes:", [route.path for route in app.routes])
