import fitz  # PyMuPDF

def extract_pages_and_images(uploaded_file):
    """
    Returns:
    - page_images: list of PNG bytes (for preview)
    - page_texts: list of German text per page
    """
    pdf_data = uploaded_file.read()
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    page_images = []
    page_texts = []

    for page in doc:
        # Extract text per page
        page_texts.append(page.get_text())

        # Render page as image
        pix = page.get_pixmap(dpi=150)
        page_images.append(pix.tobytes("png"))

    return page_images, page_texts

