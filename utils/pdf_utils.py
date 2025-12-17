import fitz  # PyMuPDF

def extract_pages_and_images(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    page_images = []
    page_texts = []

    for page in doc:
        page_texts.append(page.get_text())
        pix = page.get_pixmap(dpi=150)
        page_images.append(pix.tobytes("png"))

    return page_images, page_texts

