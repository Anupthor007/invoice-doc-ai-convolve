# utils/field_extraction.py

import re

HP_REGEX = r'(\d{1,3})\s*(?:hp|h\.p)'
COST_REGEX = r'\d{1,3}(?:,\d{2,3})+'


def avg_y(line_data):
    ys = []
    for (_, bbox, _) in line_data:
        for p in bbox:
            ys.append(p[1])
    return sum(ys) / len(ys)


def extract_fields_from_lines(text_lines, image_height):

    dealer_name = ""
    model_name = ""
    horse_power = ""
    asset_cost = ""

    # --- DEALER NAME ---
    # Candidate lines in top 20% of image
    top_candidates = []
    for text, line_data in text_lines:
        if avg_y(line_data) < image_height * 0.20:
            # Prefer uppercase-heavy and alphabetic lines
            alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
            upper_ratio = sum(c.isupper() for c in text) / max(len(text), 1)
            score = alpha_ratio + upper_ratio + len(text) / 100
            top_candidates.append((score, text))

    if top_candidates:
        dealer_name = max(top_candidates, key=lambda x: x[0])[1]

    # --- MODEL NAME ---
    # Candidate lines in middle region containing digits / parentheses
    mid_candidates = []
    for text, line_data in text_lines:
        y = avg_y(line_data)
        if image_height * 0.25 < y < image_height * 0.75:
            digit_ratio = sum(c.isdigit() for c in text) / max(len(text), 1)
            paren = "(" in text or ")" in text
            score = digit_ratio + (1 if paren else 0) + len(text) / 100
            mid_candidates.append((score, text))

    if mid_candidates:
        model_name = max(mid_candidates, key=lambda x: x[0])[1]

    # --- HORSE POWER ---
    full_text = " ".join([t[0] for t in text_lines]).lower()
    hp_match = re.search(HP_REGEX, full_text)
    if hp_match:
        horse_power = hp_match.group(1)

    # --- ASSET COST ---
    cost_matches = re.findall(COST_REGEX, full_text)
    if cost_matches:
        # pick largest numeric magnitude
        asset_cost = max(cost_matches, key=lambda x: int(x.replace(",", "")))

    return {
        "dealer_name": dealer_name.strip(),
        "model_name": model_name.strip(),
        "horse_power": horse_power.strip(),
        "asset_cost": asset_cost.strip()
    }
