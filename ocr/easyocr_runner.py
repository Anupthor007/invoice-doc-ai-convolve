import easyocr

reader = easyocr.Reader(['en','hi'])

def run_easyocr(image_path):
    result = reader.readtext(image_path)
    words = []
    boxes = []

    for (bbox, text, conf) in result:
        x = [p[0] for p in bbox]
        y = [p[1] for p in bbox]
        box = [
            int(min(x)), int(min(y)),
            int(max(x)), int(max(y))
        ]
        words.append(text)
        boxes.append(box)

    return words, boxes
