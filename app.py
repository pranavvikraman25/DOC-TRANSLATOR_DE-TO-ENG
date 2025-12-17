import streamlit as st

from utils.pdf_utils import extract_text
from utils.translate_utils import translate_text
from utils.export_utils import export_pdf, export_word, export_excel
from utils.voice_utils import text_to_voice

st.set_page_config(page_title="German Module Translator", layout="wide")

st.title("📘 German Module Handbook → English")

uploaded_file = st.file_uploader(
    "Upload German PDF / DOCX",
    type=["pdf", "docx"]
)

if uploaded_file:
    with st.spinner("Extracting text..."):
        german_text = extract_text(uploaded_file)

    with st.spinner("Translating to English..."):
        english_text = translate_text(german_text)

    st.subheader("📄 English Preview")
    edited_text = st.text_area(
        "You can highlight / edit here before download",
        english_text,
        height=350
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬇ Download PDF"):
            path = export_pdf(edited_text)
            with open(path, "rb") as f:
                st.download_button("Download PDF", f, "translated.pdf")

    with col2:
        if st.button("⬇ Download Word"):
            path = export_word(edited_text)
            with open(path, "rb") as f:
                st.download_button("Download Word", f, "translated.docx")

    with col3:
        if st.button("⬇ Download Excel"):
            path = export_excel(edited_text)
            with open(path, "rb") as f:
                st.download_button("Download Excel", f, "translated.xlsx")

    st.divider()

    if st.button("🔊 Read Aloud"):
        voice_file = text_to_voice(edited_text)
        st.audio(voice_file)
