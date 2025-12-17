import fitz
import base64

def render_pdf_pages(uploaded_file):
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=120)
        img_base64 = base64.b64encode(
            pix.tobytes("png")
        ).decode()
        pages.append(img_base64)

    return pages
