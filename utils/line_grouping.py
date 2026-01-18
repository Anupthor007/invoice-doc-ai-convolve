# utils/line_grouping.py

def group_ocr_lines(ocr_data, y_threshold=15):
    """
    Groups OCR words into lines based on vertical proximity.
    Returns list of lines, each line = list of (text, bbox)
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
    current_line = []

    for text, bbox, y in items:
        if not current_line:
            current_line.append((text, bbox, y))
            continue

        _, _, last_y = current_line[-1]

        if abs(y - last_y) <= y_threshold:
            current_line.append((text, bbox, y))
        else:
            lines.append(current_line)
            current_line = [(text, bbox, y)]

    if current_line:
        lines.append(current_line)

    # Convert to text lines
    text_lines = []
    for line in lines:
        line_text = " ".join([w[0] for w in line])
        text_lines.append((line_text, line))

    return text_lines
