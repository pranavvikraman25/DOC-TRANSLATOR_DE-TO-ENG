import streamlit as st

from utils.pdf_utils import extract_pages_and_images
from utils.translate_utils import translate_text
from utils.table_utils import extract_and_translate_tables, table_to_html
from utils.export_utils import export_pdf, export_word
from utils.voice_utils import text_to_voice


st.set_page_config(page_title="German PDF → English", layout="wide")

st.title("German Module Handbook → English")

uploaded_file = st.file_uploader("Upload German PDF", type=["pdf"])

if uploaded_file:
    pdf_bytes = uploaded_file.read()

    with open("temp.pdf", "wb") as f:
        f.write(pdf_bytes)

    tables_per_page = extract_and_translate_tables("temp.pdf")

    page_images, german_pages = extract_pages_and_images(pdf_bytes)

    translated_pages = []
    for page_text in german_pages:
        if page_text.strip():
            translated_pages.append(translate_text(page_text))
        else:
            translated_pages.append("")

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("Original PDF (German)")
        for img in page_images:
            st.image(img, use_column_width=True)

    with right_col:
        st.subheader("English Curriculum Tables")

        for page_index, page_tables in enumerate(tables_per_page):
            if not page_tables:
                continue

            st.markdown(f"### Section {page_index + 1}")

            for table in page_tables:
                st.markdown(
                    f"""
                    <div style="
                        overflow-x:auto;
                        background:white;
                        padding:16px;
                        margin-bottom:24px;
                        border-radius:8px;
                        box-shadow:0 2px 6px rgba(0,0,0,0.15);
                    ">
                    {table_to_html(table)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    final_text = "\n\n".join(translated_pages)

    col1, col2 = st.columns(2)

    with col1:
        pdf_path = export_pdf(final_text)
        with open(pdf_path, "rb") as f:
            st.download_button("Download English PDF", f, "english.pdf")

    with col2:
        word_path = export_word(final_text)
        with open(word_path, "rb") as f:
            st.download_button("Download English Word", f, "english.docx")

    if st.button("Read English Content Aloud"):
        voice_file = text_to_voice(final_text)
        st.audio(voice_file)
