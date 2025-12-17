import streamlit as st
import streamlit.components.v1 as components

from utils.pdf_utils import extract_pages_and_images
from utils.translate_utils import translate_text
from utils.export_utils import export_pdf, export_word
from utils.table_utils import extract_and_translate_tables, table_to_html
from utils.voice_utils import text_to_voice


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="German Module Handbook → English",
    layout="wide"
)

st.title("📘 German PDF → English (Module Handbook Translator)")
st.caption("Clean English result • Tables preserved • Student-friendly")


# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload German PDF",
    type=["pdf"]
)


# ---------------- MAIN LOGIC ----------------
if uploaded_file:

    # ✅ Read PDF ONCE (important)
    pdf_bytes = uploaded_file.read()

    # Save for table extraction (pdfplumber needs file path)
    with open("temp.pdf", "wb") as f:
        f.write(pdf_bytes)

    # ---------------- TABLE EXTRACTION ----------------
    with st.spinner("Detecting and translating tables..."):
        tables_per_page = extract_and_translate_tables("temp.pdf")

    # ---------------- PAGE + TEXT EXTRACTION ----------------
    with st.spinner("Reading PDF and extracting pages..."):
        page_images, german_pages = extract_pages_and_images(pdf_bytes)

    # ---------------- TRANSLATION ----------------
    translated_pages = []
    with st.spinner("Translating content to English..."):
        for page_text in german_pages:
            if page_text.strip():
                translated_pages.append(translate_text(page_text))
            else:
                translated_pages.append("")

    st.success("Translation completed successfully ✅")

    # ---------------- LAYOUT ----------------
    left_col, right_col = st.columns([1, 2])

    # ========== LEFT: ORIGINAL PDF ==========
    with left_col:
        st.markdown("### 📄 Original PDF (German)")
        st.caption("Reference view")

        for img in page_images:
            st.image(img, use_column_width=True)

    # ========== RIGHT: ENGLISH RESULT ==========
    with right_col:
        st.markdown("### 🇬🇧 English Translated Content")

        # ---- English Text (ONLY English) ----
        full_english_text = "\n\n".join(translated_pages)

        st.markdown(
            f"""
            <div style="
                font-size:18px;
                line-height:1.7;
                color:#222;
            ">
            {full_english_text.replace(chr(10), "<br>")}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---- Tables (Translated & Structured) ----
        st.markdown("### 📊 Tables (Translated)")
        for page_tables in tables_per_page:
            for table in page_tables:
                st.markdown(
                    table_to_html(table),
                    unsafe_allow_html=True
                )

    # ---------------- EXPORT ----------------
    st.divider()
    st.subheader("⬇ Download English Version")

    col1, col2 = st.columns(2)

    with col1:
        pdf_path = export_pdf(full_english_text)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download PDF (English)",
                f,
                "translated_english.pdf"
            )

    with col2:
        word_path = export_word(full_english_text)
        with open(word_path, "rb") as f:
            st.download_button(
                "📝 Download Word (English)",
                f,
                "translated_english.docx"
            )

    # ---------------- VOICE ----------------
    st.divider()
    if st.button("🔊 Read English Content Aloud"):
        voice_file = text_to_voice(full_english_text)
        st.audio(voice_file)
