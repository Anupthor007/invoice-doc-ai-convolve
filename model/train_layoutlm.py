import json
import torch
from torch.utils.data import Dataset
from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
from PIL import Image
from tqdm import tqdm

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_NAME = "microsoft/layoutlmv3-base"
LABELS = ["O", "DEALER", "MODEL", "HP", "COST"]

label2id = {l:i for i,l in enumerate(LABELS)}
id2label = {i:l for i,l in enumerate(LABELS)}

processor = LayoutLMv3Processor.from_pretrained(MODEL_NAME)
model = LayoutLMv3ForTokenClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS),
    id2label=id2label,
    label2id=label2id
).to(DEVICE)


class InvoiceDataset(Dataset):
    def __init__(self, ocr_json, annotations_json, image_folder):
        self.ocr = json.load(open(ocr_json))
        self.ann = json.load(open(annotations_json))
        self.image_folder = image_folder
        self.files = list(self.ann.keys())

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        fname = self.files[idx]
        image = Image.open(f"{self.image_folder}/{fname}").convert("RGB")

        tokens = self.ocr[fname]
        words = [t["text"] for t in tokens]
        boxes = [t["bbox"] for t in tokens]

        # Assign labels by string match (simple but works for training)
        gt = self.ann[fname]
        word_labels = []
        for w in words:
            wl = "O"
            if w.lower() in gt["dealer_name"].lower():
                wl = "DEALER"
            elif w.lower() in gt["model_name"].lower():
                wl = "MODEL"
            elif w in gt["horse_power"]:
                wl = "HP"
            elif w.replace(",","") in gt["asset_cost"]:
                wl = "COST"
            word_labels.append(label2id[wl])

        encoding = processor(
            image,
            words,
            boxes=boxes,
            word_labels=word_labels,
            truncation=True,
            return_tensors="pt"
        )

        return {k:v.squeeze(0) for k,v in encoding.items()}


def train():
    dataset = InvoiceDataset(
        "data/ocr_tokens.json",
        "data/annotations.json",
        "data/train_images"
    )

    loader = torch.utils.data.DataLoader(dataset, batch_size=2, shuffle=True)

    optim = torch.optim.AdamW(model.parameters(), lr=5e-5)

    model.train()
    for epoch in range(3):
        loop = tqdm(loader)
        for batch in loop:
            for k in batch:
                batch[k] = batch[k].to(DEVICE)

            outputs = model(**batch)
            loss = outputs.loss

            loss.backward()
            optim.step()
            optim.zero_grad()

            loop.set_description(f"Epoch {epoch}")
            loop.set_postfix(loss=loss.item())

    model.save_pretrained("model/layoutlm_finetuned")
    processor.save_pretrained("model/layoutlm_finetuned")
    print("Model saved!")


if __name__ == "__main__":
    train()
