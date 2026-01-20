from paddleocr import PaddleOCR
import cv2

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def run_ocr(image_path):
    img = cv2.imread(image_path)
    result = ocr.ocr(img)
    tokens = []

    for line in result:
        for word in line:
            bbox = word[0]
            text = word[1][0]
            tokens.append({
                "text": text,
                "bbox": bbox
            })

    return tokens
