# utils/ocr_engine.py

from paddleocr import PaddleOCR
import cv2

# Initialize OCR model once
ocr_model = PaddleOCR(use_angle_cls=True, lang='en')

def run_ocr(image_path):
    """
    Takes an image path
    Returns extracted text list with bounding boxes
    """

    image = cv2.imread(image_path)
    result = ocr_model.ocr(image, cls=True)

    ocr_data = []

    for line in result:
        for word in line:
            bbox = word[0]      # bounding box
            text = word[1][0]   # recognized text
            confidence = word[1][1]

            ocr_data.append({
                "text": text,
                "bbox": bbox,
                "confidence": confidence
            })

    return ocr_data
