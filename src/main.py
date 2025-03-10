import io
import torch

from PIL import Image
from fastapi import FastAPI, File, UploadFile
from transformers import TableTransformerForObjectDetection, DetrImageProcessor

app = FastAPI()

model_name = "microsoft/table-transformer-detection"
model = TableTransformerForObjectDetection.from_pretrained(model_name)
feature_extractor = DetrImageProcessor()

# Ensure model is on CUDA if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


@app.get('/')
def health_check():
    return {"message": 'Document Parser - AI Agent is running fine!'}


@app.post("/detect-table-bounding-box")
async def detect_table_bounding_box(file: UploadFile = File(...)):
    file_bytes = io.BytesIO(await file.read())
    image = Image.open(file_bytes).convert("RGB")

    encoding = feature_extractor(images=image, return_tensors="pt")
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
