# utils/postprocess.py

import re
from rapidfuzz import fuzz

# Keywords to anchor fields
DEALER_KEYWORDS = ["agro", "industries", "corporation", "ltd", "bank"]
MODEL_KEYWORDS = ["tractor", "kubota", "mahindra", "sonalika"]
HP_KEYWORDS = ["hp"]
COST_PATTERN = r"\d{1,3}(?:,\d{2,3})+"

def extract_fields(words):

    full_text = " ".join(words).lower()

    dealer_name = ""
    model_name = ""
    horse_power = ""
    asset_cost = ""

    # Dealer name = longest line containing dealer keywords
    for w in words:
        lw = w.lower()
        if any(k in lw for k in DEALER_KEYWORDS) and len(w) > len(dealer_name):
            dealer_name = w

    # Model name
    for w in words:
        lw = w.lower()
        if any(k in lw for k in MODEL_KEYWORDS):
            model_name = w
            break

    # Horse power
    hp_match = re.search(r'(\d+)\s*hp', full_text)
    if hp_match:
        horse_power = hp_match.group(1)

    # Asset cost
    cost_match = re.findall(COST_PATTERN, full_text)
    if cost_match:
        asset_cost = cost_match[-1]

    return {
        "dealer_name": dealer_name.strip(),
        "model_name": model_name.strip(),
        "horse_power": horse_power.strip(),
        "asset_cost": asset_cost.strip()
    }
