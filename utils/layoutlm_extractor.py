# utils/layoutlm_extractor.py

from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from PIL import Image
import torch
import numpy as np

# Load processor and model
processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = LayoutLMv3ForTokenClassification.from_pretrained(
    "microsoft/layoutlmv3-base",
    num_labels=7   # we define 7 classes for our fields
)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Label mapping (we will assign meaning)
LABELS = {
    0: "O",              # Outside
    1: "DEALER_NAME",
    2: "MODEL_NAME",
    3: "HORSE_POWER",
    4: "ASSET_COST",
}

def prepare_layoutlm_input(image_path, ocr_data):
    """
    Converts OCR data + image into LayoutLMv3 input format
    """

    image = Image.open(image_path).convert("RGB")

    words = []
    boxes = []

    for item in ocr_data:
        words.append(item["text"])

        # EasyOCR bbox is 4 points — convert to [x0,y0,x1,y1]
        bbox = item["bbox"]
        x_coords = [point[0] for point in bbox]
        y_coords = [point[1] for point in bbox]
        x0, y0, x1, y1 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)

        boxes.append([x0, y0, x1, y1])

    encoding = processor(
        image,
        words,
        boxes=boxes,
        return_tensors="pt",
        truncation=True,
        padding="max_length"
    )

    return encoding


def extract_fields_layoutlm(image_path, ocr_data):
    """
    Runs LayoutLMv3 and returns token-level predictions
    """

    encoding = prepare_layoutlm_input(image_path, ocr_data)

    encoding = {k: v.to(device) for k, v in encoding.items()}

    with torch.no_grad():
        outputs = model(**encoding)

    predictions = outputs.logits.argmax(-1).squeeze().tolist()
    tokens = processor.tokenizer.convert_ids_to_tokens(encoding["input_ids"].squeeze().tolist())

    extracted = {
        "DEALER_NAME": [],
        "MODEL_NAME": [],
        "HORSE_POWER": [],
        "ASSET_COST": []
    }

    for token, label_id in zip(tokens, predictions):
        label = LABELS[label_id]

        if label != "O":
            extracted[label].append(token.replace("▁", ""))

    # Join token pieces
    final = {k: " ".join(v).strip() for k, v in extracted.items()}

    return final
