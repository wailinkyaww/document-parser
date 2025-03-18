from ultralyticsplus import YOLO
from ..apps.logger import get_logger

logger = get_logger(__file__)


def load_model(device: str):
    # Load YOLOv8 model
    model = YOLO("keremberke/yolov8m-table-extraction")

    model.overrides["conf"] = 0.25  # Confidence threshold
    model.overrides["iou"] = 0.45  # IoU threshold
    model.overrides["agnostic_nms"] = False  # Non-class specific detection
    model.overrides["max_det"] = 1000  # Maximum detections per image
    model.overrides["device"] = device  # GPU / CPU

    return model
