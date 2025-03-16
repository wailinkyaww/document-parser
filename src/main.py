from .apps.config import initialize_config

# This should run before we do anything.
initialize_config()

import io
import torch

from PIL import Image
from fastapi import FastAPI, File, UploadFile

from .models import load_model
from .apps.logger import get_logger
from .middlewares.authenticate_request import AuthenticateRequestMiddleware

# Ensure model is on CUDA if available
device = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI()
logger = get_logger(__file__)
image_processor, model = load_model(device)

app.add_middleware(AuthenticateRequestMiddleware)


@app.get('/')
def health_check():
    return {"message": 'Document Parser is running fine!'}


@app.post("/detect-table-bounding-box")
async def detect_table_bounding_box(file: UploadFile = File(...)):
    file_bytes = io.BytesIO(await file.read())
    image = Image.open(file_bytes).convert("RGB")

    logger.info('Encoding the incoming image.')
    encoding = image_processor(images=image, return_tensors="pt")
    encoding = {k: v.to(device) for k, v in encoding.items()}

    # Perform inference Only
    logger.info('Running table detection on the image.')
    with torch.no_grad():
        outputs = model(**encoding)

    logger.info('Extracting bounding boxes from results.')
    results = outputs.logits[0].softmax(-1)
    keep = results[:, :-1].max(-1).values > 0.5  # Confidence threshold
    boxes = outputs.pred_boxes[0][keep].cpu().numpy()

    bounding_boxes = [{"x": float(x), "y": float(y), "width": float(w), "height": float(h)} for x, y, w, h in boxes]
    logger.debug(f'Detection completed - bounding boxes {bounding_boxes}')

    return {"table_bounding_boxes": bounding_boxes}
