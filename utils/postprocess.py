# utils/postprocess.py

import re

def clean_fields(fields):

    # Clean Dealer Name
    dealer = fields["DEALER_NAME"]

    # Clean Model Name
    model = fields["MODEL_NAME"]

    # Horse Power numeric
    hp = fields["HORSE_POWER"]
    hp_match = re.search(r'\d+', hp)
    horse_power = hp_match.group() if hp_match else ""

    # Asset Cost numeric with commas
    cost = fields["ASSET_COST"]
    cost_match = re.findall(r'\d{1,3}(?:,\d{2,3})+', cost.replace(" ", ""))
    asset_cost = cost_match[-1] if cost_match else ""

    return {
        "dealer_name": dealer,
        "model_name": model,
        "horse_power": horse_power,
        "asset_cost": asset_cost
    }
