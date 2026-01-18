import sys, json
from utils.ocr_engine import run_ocr
from utils.layoutlm_extractor import extract_layoutlm_embeddings
from utils.postprocess import extract_fields

def main():
    image_path = sys.argv[1]

    ocr_data = run_ocr(image_path)

    words, embeddings = extract_layoutlm_embeddings(image_path, ocr_data)

    fields = extract_fields(words)

    with open("output.json","w",encoding="utf-8") as f:
        json.dump(fields, f, indent=4, ensure_ascii=False)

    print("output.json saved")

if __name__ == "__main__":
    main()
