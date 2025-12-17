import streamlit as st

from utils.pdf_utils import extract_pages_and_images
from utils.translate_utils import translate_text
from utils.export_utils import export_pdf, export_word, export_excel
from utils.voice_utils import text_to_voice

st.set_page_config(
    page_title="German Module Translator",
    layout="wide"
)

st.title("📘 German PDF → English (Module Handbook Translator)")

uploaded_file = st.file_uploader(
    "Upload German PDF",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Reading PDF and extracting pages..."):
        page_images, german_pages = extract_pages_and_images(uploaded_file)

    translated_pages = []

    with st.spinner("Translating page by page..."):
        for page_text in german_pages:
            if page_text.strip():
                translated_pages.append(translate_text(page_text))
            else:
                translated_pages.append("")

    st.success("Translation completed")

    st.divider()
    st.subheader("📄 PDF-like Preview with English Translation")

    edited_pages = []

    for i in range(len(page_images)):
        st.markdown(f"### Page {i+1}")

        # Show original PDF page as image
        st.image(page_images[i], use_column_width=True)

        # Show English translation
        edited_text = st.text_area(
            f"English Translation – Page {i+1}",
            translated_pages[i],
            height=220
        )

        edited_pages.append(edited_text)
        st.divider()

    final_text = "\n\n".join(edited_pages)

    st.subheader("⬇ Download Translated Document")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Download PDF"):
            path = export_pdf(final_text)
            with open(path, "rb") as f:
                st.download_button(
                    "Download PDF",
                    f,
                    "translated.pdf"
                )

    with col2:
        if st.button("Download Word"):
            path = export_word(final_text)
            with open(path, "rb") as f:
                st.download_button(
                    "Download Word",
                    f,
                    "translated.docx"
                )

    with col3:
        if st.button("Download Excel"):
            path = export_excel(final_text)
            with open(path, "rb") as f:
                st.download_button(
                    "Download Excel",
                    f,
                    "translated.xlsx"
                )

    st.divider()

    if st.button("🔊 Read Full Translation Aloud"):
        voice_file = text_to_voice(final_text)
        st.audio(voice_file)
