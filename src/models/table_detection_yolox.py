import torch
from pandas.conftest import utc_fixture
from ultralyticsplus import YOLO
from ultralytics.nn import  tasks

from ..apps.logger import get_logger

logger = get_logger(__file__)


def load_model(device: str):
    logger.info('Loading yolov8m-table-extraction model...')

    model = YOLO("keremberke/yolov8m-table-extraction")

    # PyTorch 2.6+ introduced a stricter security policy when loading model weights,
    # YOLOv8 model checkpoint likely contains additional metadata beyond just the weights
    torch.serialization.add_safe_globals([tasks.DetectionModel])


    model.overrides["conf"] = 0.25  # Confidence threshold
    model.overrides["iou"] = 0.45  # IoU threshold
    model.overrides["agnostic_nms"] = False  # Non-class specific detection
    model.overrides["max_det"] = 1000  # Maximum detections per image

    logger.info('Model loaded successfully.')

    return model
