# utils/ocr_engine.py

import easyocr
import cv2

# Initialize EasyOCR once
reader = easyocr.Reader(['en','hi'], gpu=True)  # works on Colab GPU

def run_ocr(image_path):
    """
    Takes image path
    Returns extracted text with bounding boxes and confidence
    """

    image = cv2.imread(image_path)
    results = reader.readtext(image)

    ocr_data = []
    for (bbox, text, confidence) in results:
        ocr_data.append({
            "text": text,
            "bbox": bbox,
            "confidence": confidence
        })

    return ocr_data
