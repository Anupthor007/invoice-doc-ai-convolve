import re
from rapidfuzz import fuzz

def find_near(tokens, keyword, thresh=70):
    best = None
    for t in tokens:
        if fuzz.partial_ratio(t["text"].lower(), keyword.lower()) > thresh:
            best = t
    return best

def extract_fields(tokens):
    out = {
        "dealer_name": "",
        "model_name": "",
        "horse_power": "",
        "asset_cost": ""
    }

    # Dealer name → largest text near top
    top_texts = [t for t in tokens if t["bbox"][1] < 300]
    top_texts.sort(key=lambda x: len(x["text"]), reverse=True)
    if top_texts:
        out["dealer_name"] = top_texts[0]["text"]

    # Model name → text containing Tractor / Model
    for t in tokens:
        if re.search(r"(tractor|model|mahindra|eicher|swaraj)", t["text"].lower()):
            out["model_name"] = t["text"]
            break

    # Horse power → HP pattern
    for t in tokens:
        m = re.search(r"(\d{2,3})\s*hp", t["text"].lower())
        if m:
            out["horse_power"] = m.group(1)
            break

    # Asset cost → biggest currency number
    amounts = []
    for t in tokens:
        if re.search(r"\d{1,2}[,]\d{2,3}[,]\d{3}", t["text"]):
            val = re.sub(r"[^\d]", "", t["text"])
            amounts.append(int(val))
    if amounts:
        out["asset_cost"] = str(max(amounts))

    return out
