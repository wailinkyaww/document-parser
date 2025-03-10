from ..apps.logger import get_logger
from transformers import TableTransformerForObjectDetection, DetrImageProcessor

logger = get_logger(__file__)
model_name = "microsoft/table-transformer-detection"


def load_model(device: str):
    logger.info("Loading Table Transformer model...")

    model = TableTransformerForObjectDetection.from_pretrained(model_name)
    image_processor = DetrImageProcessor()
    model.to(device)

    logger.info("Model loaded successfully.")

    return image_processor, model
