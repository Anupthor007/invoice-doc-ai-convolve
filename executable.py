import easyocr

reader = easyocr.Reader(['en','hi'])

def run_easyocr(image_path):
    result = reader.readtext(image_path)
    tokens = []

    for (bbox, text, conf) in result:
        x_coords = [p[0] for p in bbox]
        y_coords = [p[1] for p in bbox]
        box = [
            int(min(x_coords)),
            int(min(y_coords)),
            int(max(x_coords)),
            int(max(y_coords))
        ]
        tokens.append({
            "text": text,
            "bbox": box,
            "confidence": float(conf)
        })

    return tokens
