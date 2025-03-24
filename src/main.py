from .apps.config import initialize_config

# This should run before we do anything.
initialize_config()

import io
import torch

from PIL import Image
from fastapi import FastAPI, File, UploadFile

from .models import load_table_detection_yolox_model
from .services import YoloV8TableDetector
from .apps.logger import get_logger
from .middlewares.authenticate_request import AuthenticateRequestMiddleware

app = FastAPI()
logger = get_logger(__file__)

# Ensure model is on CUDA if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_table_detection_yolox_model(device)
table_detector = YoloV8TableDetector(model)

app.add_middleware(AuthenticateRequestMiddleware)


@app.get('/')
def health_check():
    return {"message": 'Document Parser is running fine!'}


@app.post("/detect-table-bounding-boxes")
async def detect_table_bounding_box(file: UploadFile = File(...)):
    file_bytes = io.BytesIO(await file.read())
    image = Image.open(file_bytes).convert("RGB")

    logger.info('Running table detection on the image.')
    bboxes = table_detector.detect(image)

    logger.info('Got table detection results.')
    logger.debug(f'Detection completed - bounding boxes {bboxes}')

    return {"table_bounding_boxes": bboxes}
