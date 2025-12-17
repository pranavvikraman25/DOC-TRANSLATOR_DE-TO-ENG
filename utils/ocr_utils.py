import pytesseract
from PIL import Image
import io
import numpy as np

def ocr_with_boxes(image_bytes):
    try:
        pytesseract.get_tesseract_version()
    except:
        raise RuntimeError("TESSERACT_NOT_AVAILABLE")

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = np.array(image)

    data = pytesseract.image_to_data(
        img,
        lang="deu",
        output_type=pytesseract.Output.DICT
    )

    boxes = []
    for i in range(len(data["text"])):
        text = data["text"][i].strip()
        if text:
            boxes.append({
                "text": text,
                "x": data["left"][i],
                "y": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i],
            })

    return boxes
