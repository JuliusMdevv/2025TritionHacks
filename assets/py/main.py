from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from ultralytics import YOLO

app = FastAPI()

# Enable CORS so frontend can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLOv8 model (nano for speed, or use yolov8m/yolov8l for better accuracy)
model = YOLO("yolov8n.pt")


# Define class names that trigger emergency
CRIME_CLASSES = {
    "knife",
    "gun",           # If the model supports it
    "fire",
    "fight",         # You'll need logic for multiple people close together
    "smoke"
}

FIRST_RESPONDER_CLASSES = {
    "knife", "gun", "fire", "smoke", "fight"
}

PERSON_CLASS = {
    "person"
}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    # try:
    #     contents = await file.read()
    #     nparr = np.frombuffer(contents, np.uint8)
    #     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    #     # Run detection
    #     results = model(img)[0]
    #     names = model.names
    #     detected_labels = [names[int(box.cls)] for box in results.boxes]

    #     # Logic
    #     emergency = any(obj in FIRST_RESPONDER_CLASSES for obj in detected_labels)
    #     crime = any(obj in CRIME_CLASSES for obj in detected_labels)
    #     person = any(obj in PERSON_CLASS for obj in detected_labels)

    #     if emergency:
    #         status = "First Responder Needed"
    #     elif person:
    #         status = "Person Detected"
    #     else:
    #         status = "No Crime"

    #     return {"status": status, "objects": detected_labels}
    # except Exception as e:
    #     return JSONResponse(status_code=500, content={"error": str(e)})

    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Run detection
        results = model(img)[0]
        names = model.names
        detected_labels = [names[int(box.cls)] for box in results.boxes]

        # Count people
        person_count = detected_labels.count("person")

        # Logic
        emergency = any(obj in FIRST_RESPONDER_CLASSES for obj in detected_labels)
        crime = any(obj in CRIME_CLASSES for obj in detected_labels)

        if emergency:
            status = "First Responder Needed"
        elif person_count == 1:
            status = f"{person_count} Person Detected"
        elif person_count > 1:
            status = f"{person_count} People Detected"
        else:
            status = "No Emergency"

        return {
            "status": status,
            "objects": detected_labels,
            "person_count": person_count
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})