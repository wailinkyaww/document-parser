import numpy as np

from typing import List, Dict
from PIL.ImageFile import ImageFile
from abc import ABC, abstractmethod
from ultralyticsplus import YOLO


class BoundingBox:
    """Represents a bounding box with x, y, width, and height."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def to_dict(self) -> Dict[str, float]:
        """Convert bounding box to a dictionary format."""
        return {
            "x": float(self.x),
            "y": float(self.y),
            "width": float(self.width),
            "height": float(self.height)
        }

    def __repr__(self):
        return f"BoundingBox(x={self.x}, y={self.y}, width={self.width}, height={self.height})"


class TableDetector(ABC):
    @abstractmethod
    def detect(self, image: ImageFile) -> List[BoundingBox]:
        """
        Detect tables in the given image and return a list of bounding boxes.

        :param image: Input image (PIL ImageFile)
        :return: List of BoundingBox identified in the image
        """
        pass


class YoloV8TableDetector(TableDetector):
    def __init__(self, model: YOLO):
        self.model = model

    def detect(self, image: ImageFile) -> List[BoundingBox]:
        # Convert PIL image to OpenCV format (numpy array)
        img_cv = np.array(image)

        # Run inference
        results = self.model.predict(img_cv)

        bounding_boxes = []
        if len(results[0].boxes) > 0:
            for box in results[0].boxes.data.numpy():
                x1, y1, x2, y2, _, _ = map(int, box)  # Extract bounding box coordinates
                width = x2 - x1
                height = y2 - y1
                bounding_boxes.append(BoundingBox(x1, y1, width, height))

        return bounding_boxes
