# utils/layoutlm_extractor.py

from transformers import LayoutLMv3Processor, LayoutLMv3Model
from PIL import Image
import torch

processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=False)
model = LayoutLMv3Model.from_pretrained("microsoft/layoutlmv3-base")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def prepare_layoutlm_input(image_path, ocr_data):
    image = Image.open(image_path).convert("RGB")

    words = []
    boxes = []

    for item in ocr_data:
        words.append(item["text"])

        bbox = item["bbox"]
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        x0, y0, x1, y1 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)

        # --- KEY FIX: normalize to 0–1000 and convert to int ---
        width, height = image.size
        x0 = int(1000 * x0 / width)
        x1 = int(1000 * x1 / width)
        y0 = int(1000 * y0 / height)
        y1 = int(1000 * y1 / height)

        boxes.append([x0, y0, x1, y1])

    encoding = processor(
        image,
        words,
        boxes=boxes,
        return_tensors="pt",
        truncation=True,
        padding="max_length"
    )

    return encoding, words


def extract_layoutlm_embeddings(image_path, ocr_data):
    encoding, words = prepare_layoutlm_input(image_path, ocr_data)
    encoding = {k: v.to(device) for k, v in encoding.items()}

    with torch.no_grad():
        outputs = model(**encoding)

    # last_hidden_state = contextualized token embeddings
    embeddings = outputs.last_hidden_state.squeeze(0).cpu()

    return words, embeddings
