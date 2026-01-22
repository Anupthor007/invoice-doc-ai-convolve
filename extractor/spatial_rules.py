import re

def extract_fields(tokens):

    dealer_name = ""
    model_name = ""
    horse_power = ""
    asset_cost = ""

    # --- Dealer name: longest text near top ---
    top = [t for t in tokens if t["bbox"][1] < 300]
    if top:
        dealer_name = max(top, key=lambda x: len(x["text"]))["text"]

    # --- Model name: first line containing tractor / model ---
    for t in tokens:
        if re.search(r"(tractor|model|mahindra|swaraj|eicher|kubota)", t["text"].lower()):
            model_name = t["text"]
            break

    # --- Horse power ---
    for t in tokens:
        m = re.search(r"(\d{2,3})\s*hp", t["text"].lower())
        if m:
            horse_power = m.group(1)
            break

    # --- Asset cost: largest currency number ---
    nums = []
    for t in tokens:
        if re.search(r"\d{1,3}(?:,\d{2,3})+", t["text"]):
            val = int(t["text"].replace(",", ""))
            nums.append(val)

    if nums:
        asset_cost = str(max(nums))

    return {
        "dealer_name": dealer_name.strip(),
        "model_name": model_name.strip(),
        "horse_power": horse_power.strip(),
        "asset_cost": asset_cost.strip()
    }
