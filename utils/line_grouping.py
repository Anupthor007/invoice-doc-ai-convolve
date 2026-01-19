# utils/line_grouping.py

def group_ocr_lines(ocr_data, y_threshold=12):
    """
    Groups OCR words into lines using vertical proximity.
    Returns list of tuples: (line_text, line_data)
    """

    items = []
    for item in ocr_data:
        bbox = item["bbox"]
        y_coords = [p[1] for p in bbox]
        y_center = sum(y_coords) / 4
        items.append((item["text"], bbox, y_center))

    # Sort by vertical position
    items.sort(key=lambda x: x[2])

    lines = []
    current = []

    for text, bbox, y in items:
        if not current:
            current.append((text, bbox, y))
            continue

        if abs(y - current[-1][2]) <= y_threshold:
            current.append((text, bbox, y))
        else:
            lines.append(current)
            current = [(text, bbox, y)]

    if current:
        lines.append(current)

    # Build final text lines
    text_lines = []
    for line in lines:
        line_text = " ".join([w[0] for w in line])
        text_lines.append((line_text, line))

    return text_lines
