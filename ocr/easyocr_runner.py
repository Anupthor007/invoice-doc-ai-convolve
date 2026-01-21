import easyocr
import json
import os
from PIL import Image

reader = easyocr.Reader(['en','hi'])   # English + Hindi (vernacular)

def run_easyocr(image_path):
    result = reader.readtext(image_path)

    tokens = []
    for (bbox, text, conf) in result:
        # bbox = [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        box = [
            int(min(x_coords)),
            int(min(y_coords)),
            int(max(x_coords)),
            int(max(y_coords))
        ]
        tokens.append({
            "text": text,
            "bbox": box,
            "confidence": conf
        })

    return tokens


def process_folder(image_folder, output_json):
    data = {}
    for img in os.listdir(image_folder):
        if img.lower().endswith(".png"):
            path = os.path.join(image_folder, img)
            tokens = run_easyocr(path)
            data[img] = tokens

    with open(output_json,"w") as f:
        json.dump(data,f,indent=2)

    print("OCR tokens saved:", output_json)


if __name__ == "__main__":
    process_folder("data/train_images", "data/ocr_tokens.json")
