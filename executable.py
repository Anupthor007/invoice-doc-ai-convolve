import sys
import json
from PIL import Image
from ocr.easyocr_runner import run_easyocr
from model.infer_layoutlm import infer

def main():
    image_path = sys.argv[1]

    image = Image.open(image_path).convert("RGB")
    words, boxes = run_easyocr(image_path)

    result = infer(image, words, boxes)

    with open("output.json","w") as f:
        json.dump(result,f,indent=2)

    print("output.json saved")

if __name__ == "__main__":
    main()
