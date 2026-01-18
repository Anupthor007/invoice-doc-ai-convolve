import sys
import json

from utils.ocr_engine import run_ocr
from utils.layoutlm_extractor import extract_fields_layoutlm
from utils.postprocess import clean_fields

def main():

    image_path = sys.argv[1]

    # OCR
    ocr_data = run_ocr(image_path)

    # LayoutLMv3 extraction
    raw_fields = extract_fields_layoutlm(image_path, ocr_data)

    # Post-process cleanup
    final_fields = clean_fields(raw_fields)

    # Save output.json
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(final_fields, f, indent=4, ensure_ascii=False)

    print("Saved output.json")

if __name__ == "__main__":
    main()
