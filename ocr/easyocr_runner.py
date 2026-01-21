import easyocr
import json
import os

reader = easyocr.Reader(['en','hi'])  # English + Hindi

def run_easyocr(image_path):
    result = reader.readtext(image_path)
    tokens = []

    for (bbox, text, conf) in result:
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
            "confidence": float(conf)
        })

    return tokens


def process_folder(image_folder, output_json):
    data = {}
    images = [img for img in os.listdir(image_folder) if img.lower().endswith(".png")]

    print(f"Found {len(images)} images. Running OCR...")

    for img in images:
        path = os.path.join(image_folder, img)
        tokens = run_easyocr(path)
        data[img] = tokens

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("OCR completed. Saved to:", output_json)


# ---- MAIN EXECUTION ----
if __name__ == "__main__":
    process_folder("data/train_images", "data/ocr_tokens.json")
