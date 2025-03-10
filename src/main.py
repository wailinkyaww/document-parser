import io
import torch

from fastapi import FastAPI, File, UploadFile
from transformers import TableTransformerForObjectDetection, TableTransformerImageProcessor
from PIL import Image

app = FastAPI()


@app.get('/')
def health_check():
    return {"message": 'Document Parser - AI Agent is running fine!'}


@app.get('/detect-table-bounding')
def detect_table_bounding_box():
    return {"table": []}


app = FastAPI()

# Load the pre-trained Table Transformer model
model_name = "microsoft/table-transformer-detection"
processor = TableTransformerImageProcessor.from_pretrained(model_name)
model = TableTransformerForObjectDetection.from_pretrained(model_name)

# Ensure model is on CUDA if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

@app.post("/detect-table-bounding-box")
async def detect_table_bounding_box(file: UploadFile = File(...)):
    # Read image
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    # Preprocess the image
    encoding = processor(images=image, return_tensors="pt")
    encoding = {k: v.to(device) for k, v in encoding.items()}

    # Perform inference
    with torch.no_grad():
        outputs = model(**encoding)

    # Extract bounding boxes
    results = outputs.logits[0].softmax(-1)
    keep = results[:, :-1].max(-1).values > 0.5  # Confidence threshold
    boxes = outputs.pred_boxes[0][keep].cpu().numpy()

    # Format output
    bounding_boxes = [{"x": float(x), "y": float(y), "width": float(w), "height": float(h)} for x, y, w, h in boxes]

    return {"bounding_boxes": bounding_boxes}