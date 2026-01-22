import sys, json
from ocr.easyocr_runner import run_easyocr
from extractor.spatial_rules import extract_fields

def main():
    image_path = sys.argv[1]

    tokens = run_easyocr(image_path)
    result = extract_fields(tokens)

    with open("output.json","w",encoding="utf8") as f:
        json.dump(result,f,indent=2,ensure_ascii=False)

    print("output.json saved")

if __name__ == "__main__":
    main()
