from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import docx
import pandas as pd
import tempfile

def export_pdf(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(file.name, pagesize=A4)
    y = 800
    for line in text.split("\n"):
        c.drawString(40, y, line[:100])
        y -= 15
        if y < 40:
            c.showPage()
            y = 800
    c.save()
    return file.name

def export_word(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(file.name)
    return file.name

def export_excel(text):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    df = pd.DataFrame({"Translated Text": text.split("\n")})
    df.to_excel(file.name, index=False)
    return file.name
