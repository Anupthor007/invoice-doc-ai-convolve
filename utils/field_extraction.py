# utils/field_extraction.py

import re

# Regex patterns
HP_PATTERN = r'(\d{1,3})\s*hp'
COST_PATTERN = r'\d{1,3}(?:,\d{2,3})+'

def extract_fields_from_lines(text_lines, image_height):

    dealer_name = ""
    model_name = ""
    horse_power = ""
    asset_cost = ""

    # --- Dealer Name ---
    # Pick longest text line in top 25% of document
    for line_text, line_data in text_lines:
        # compute average y of line
        ys = [p[1] for (_, bbox, _) in line_data for p in bbox]
        avg_y = sum(ys) / len(ys)

        if avg_y < image_height * 0.25:
            if len(line_text) > len(dealer_name):
                dealer_name = line_text

    # --- Model Name ---
    # Look for lines containing keyword 'tractor'
    for line_text, _ in text_lines:
        if "tractor" in line_text.lower():
            model_name = line_text
            break

    # --- Horse Power ---
    full_text = " ".join([l[0] for l in text_lines]).lower()
    hp_match = re.search(HP_PATTERN, full_text)
    if hp_match:
        horse_power = hp_match.group(1)

    # --- Asset Cost ---
    # find all numeric currency patterns
    cost_matches = re.findall(COST_PATTERN, full_text)
    if cost_matches:
        # choose last (usually total)
        asset_cost = cost_matches[-1]

    return {
        "dealer_name": dealer_name.strip(),
        "model_name": model_name.strip(),
        "horse_power": horse_power.strip(),
        "asset_cost": asset_cost.strip()
    }
