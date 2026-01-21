import torch
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from PIL import Image

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = LayoutLMv3Processor.from_pretrained("model/layoutlm_finetuned")
model = LayoutLMv3ForTokenClassification.from_pretrained(
    "model/layoutlm_finetuned"
).to(DEVICE)

id2label = model.config.id2label


def infer(image, words, boxes):
    encoding = processor(image, words, boxes=boxes, return_tensors="pt")
    for k in encoding:
        encoding[k] = encoding[k].to(DEVICE)

    outputs = model(**encoding)
    preds = outputs.logits.argmax(-1).squeeze().tolist()

    results = {"dealer_name":"","model_name":"","horse_power":"","asset_cost":""}

    for word, pred in zip(words, preds):
        label = id2label[pred]
        if label == "DEALER":
            results["dealer_name"] += word + " "
        elif label == "MODEL":
            results["model_name"] += word + " "
        elif label == "HP":
            results["horse_power"] += word + " "
        elif label == "COST":
            results["asset_cost"] += word + " "

    return results
