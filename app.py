import streamlit as st
import streamlit.components.v1 as components
import base64
from utils.ocr_utils import ocr_with_boxes
from utils.overlay_html_utils import build_overlay_html
from utils.pdf_utils import extract_pages_and_images
from utils.translate_utils import translate_text
from utils.export_utils import export_pdf, export_word
from utils.voice_utils import text_to_voice
from utils.table_utils import extract_and_translate_tables, table_to_html


# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="German Module Translator",
    layout="wide"
)

st.title("📘 German PDF → English (Module Handbook Translator)")
st.caption("Book-style preview • Long PDF safe • Student-friendly")


# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader(
    "Upload German PDF",
    type=["pdf"]
)

if uploaded_file:

    # ✅ Read PDF ONCE
    pdf_bytes = uploaded_file.read()
    
    # Save for pdfplumber (tables)
    with open("temp.pdf", "wb") as f:
        f.write(pdf_bytes)
    
    tables_per_page = extract_and_translate_tables("temp.pdf")
    
    # Use SAME bytes for PyMuPDF
    with st.spinner("Reading PDF and extracting pages..."):
        page_images, german_pages = extract_pages_and_images(pdf_bytes)




# -------------------- MAIN LOGIC --------------------
if uploaded_file:

    # 1️⃣ Extract pages + text
    with st.spinner("Reading PDF and extracting pages..."):
        page_images, german_pages = extract_pages_and_images(uploaded_file)

    # 2️⃣ Translate page by page (safe for long PDFs)
    translated_pages = []
    with st.spinner("Translating page by page..."):
        for page_text in german_pages:
            if page_text.strip():
                translated_pages.append(st.cache_data(translate_text)(page_text))

            else:
                translated_pages.append("")

    st.success("Translation completed successfully ✅")
    show_lens = st.toggle(
        "🔍 Enable Google-Lens Style Translation Layer (Hover to Translate)",
        value=False
    )

 

    # -------------------- BOOK-STYLE PREVIEW --------------------
    st.divider()
    st.subheader("📖 Book-style English Preview (Easy Reading)")

    edited_pages = []

    for i in range(len(page_images)):

        # Convert image bytes → base64
        img_base64 = base64.b64encode(page_images[i]).decode()

        # HTML for book-style page
        html_page = f"""
        <div style="
            max-width:900px;
            margin:40px auto;
            padding:30px;
            background:#f7f7f7;
            border-radius:12px;
            box-shadow:0 0 18px rgba(0,0,0,0.15);
        ">

            <div style="text-align:center; margin-bottom:20px;">
                <strong style="font-size:20px;">Page {i+1}</strong>
            </div>

            <img src="data:image/png;base64,{img_base64}"
                 style="width:100%; border-radius:8px;" />

            <hr style="margin:30px 0"/>

            <div style="
                font-family:Georgia, serif;
                font-size:18px;
                line-height:1.7;
                color:#222;
                white-space:pre-wrap;
            ">
                {translated_pages[i]}
            </div>

        </div>
        """

        components.html(
            html_page,
            height=900,
            scrolling=True
        )
        if tables_per_page[i]:
            st.markdown("### 📊 Detected Tables (Translated)")
            for table in tables_per_page[i]:
                st.markdown(
                    table_to_html(table),
                    unsafe_allow_html=True
                )
    
        st.divider()
        # ---------------- GOOGLE LENS STYLE OVERLAY ----------------
        if show_lens:
            try:
                ocr_boxes = ocr_with_boxes(page_images[i])
        
                for box in ocr_boxes:
                    try:
                        box["translated"] = translate_text(box["text"])
                    except:
                        box["translated"] = box["text"]
        
                overlay_html = build_overlay_html(img_base64, ocr_boxes)
        
                components.html(
                    overlay_html,
                    height=800,
                    scrolling=True
                )
        
            except RuntimeError:
                st.warning(
                    "🔍 Google-Lens mode requires OCR support. "
                    "This feature works locally or in Docker, "
                    "but is limited on Streamlit Cloud."
                )


        # Store text for export
        edited_pages.append(translated_pages[i])

    # -------------------- EXPORT SECTION --------------------
    final_text = "\n\n".join(edited_pages)

    st.divider()
    st.subheader("⬇ Download Translated Document")

    col1, col2, col3 = st.columns(3)

    with col1:
        path = export_pdf(final_text)
        with open(path, "rb") as f:
            st.download_button(
                "📄 Download PDF",
                f,
                "translated.pdf"
            )

    with col2:
        path = export_word(final_text)
        with open(path, "rb") as f:
            st.download_button(
                "📝 Download Word",
                f,
                "translated.docx"
            )

    # -------------------- VOICE --------------------
    st.divider()
    if st.button("🔊 Read Full Translation Aloud"):
        voice_file = text_to_voice(final_text)
        st.audio(voice_file)
