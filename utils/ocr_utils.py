import pytesseract
import cv2
import numpy as np
from PIL import Image
import io


def is_tesseract_available():
    try:
        pytesseract.get_tesseract_version()
        return True
    except:
        return False


def ocr_with_boxes(image_bytes):
    if not is_tesseract_available():
        raise RuntimeError("TESSERACT_NOT_AVAILABLE")

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = np.array(image)

    data = pytesseract.image_to_data(
        img,
        lang="deu",
        output_type=pytesseract.Output.DICT
    )

    boxes = []
    n = len(data["text"])

    for i in range(n):
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
