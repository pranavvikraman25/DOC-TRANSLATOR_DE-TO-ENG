import pdfplumber
from utils.translate_utils import translate_text

def extract_and_translate_tables(pdf_path):
    tables_per_page = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = []
            tables = page.extract_tables()

            for table in tables:
                translated_table = []
                for row in table:
                    translated_row = []
                    for cell in row:
                        if cell:
                            try:
                                translated_row.append(translate_text(cell))
                            except:
                                translated_row.append(cell)
                        else:
                            translated_row.append("")
                    translated_table.append(translated_row)
                page_tables.append(translated_table)

            tables_per_page.append(page_tables)

    return tables_per_page


def table_to_html(table):
    html = "<table style='border-collapse:collapse;width:100%'>"
    for row in table:
        html += "<tr>"
        for cell in row:
            html += f"<td style='border:1px solid #888;padding:8px'>{cell}</td>"
        html += "</tr>"
    html += "</table><br>"
    return html
