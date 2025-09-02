import streamlit as st
import pypandoc
from xhtml2pdf import pisa
import tempfile
import os

st.set_page_config(page_title="EPUB → PDF Converter", page_icon="📚")

st.title("📚 EPUB to PDF Converter")
st.write("Upload an EPUB file and convert it to a PDF (with images + formatting).")

uploaded_file = st.file_uploader("Choose an EPUB file", type=["epub"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as temp_epub:
        temp_epub.write(uploaded_file.read())
        epub_path = temp_epub.name

    html_path = epub_path.replace(".epub", ".html")
    pdf_path = epub_path.replace(".epub", ".pdf")

    try:
        st.info("Converting EPUB → HTML with Pandoc...")
        pypandoc.convert_file(epub_path, "html", outputfile=html_path)

        st.info("Converting HTML → PDF (keeping images)...")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        with open(pdf_path, "wb") as f:
            pisa.CreatePDF(html_content, dest=f)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        st.success("✅ Conversion successful (images included)!")

    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")

    finally:
        for path in [epub_path, html_path, pdf_path]:
            if os.path.exists(path):
                os.remove(path)
