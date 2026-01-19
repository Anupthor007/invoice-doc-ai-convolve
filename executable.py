import sys
import json
from PIL import Image

from utils.ocr_engine import run_ocr
from utils.line_grouping import group_ocr_lines
from utils.field_extraction import extract_fields_from_lines


def main():
    image_path = sys.argv[1]

    # Load image
    img = Image.open(image_path)
    image_height = img.size[1]

    # OCR
    ocr_data = run_ocr(image_path)

    # Group into lines
    text_lines = group_ocr_lines(ocr_data)

    # Extract fields
    fields = extract_fields_from_lines(text_lines, image_height)

    # Save JSON
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(fields, f, indent=4, ensure_ascii=False)

    print("output.json saved")


if __name__ == "__main__":
    main()
