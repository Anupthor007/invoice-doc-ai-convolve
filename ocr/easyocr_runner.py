import easyocr, json, os
from PIL import Image

reader = easyocr.Reader(['en','hi'])

def process_folder(image_folder, out_json):
    results = {}
    for img_name in os.listdir(image_folder):
        if not img_name.lower().endswith(".png"):
            continue
        path = os.path.join(image_folder, img_name)
        ocr = reader.readtext(path)
        tokens = []
        for (bbox, text, conf) in ocr:
            x_coords = [p[0] for p in bbox]
            y_coords = [p[1] for p in bbox]
            tokens.append({
                "text": text,
                "bbox": [
                    int(min(x_coords)), int(min(y_coords)),
                    int(max(x_coords)), int(max(y_coords))
                ],
                "confidence": float(conf)
            })
        results[img_name] = tokens
    
    with open(out_json,"w",encoding="utf8") as f:
        json.dump(results,f,indent=2)

if __name__ == "__main__":
    process_folder("data/train_images","data/ocr_tokens.json")
