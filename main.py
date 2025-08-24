import streamlit as st
import pypandoc
from fpdf import FPDF
from bs4 import BeautifulSoup
import tempfile
import os

st.set_page_config(page_title="EPUB → PDF Converter", page_icon="📚")
st.title("📚 EPUB to PDF Converter (Lightweight)")

uploaded_file = st.file_uploader("Upload an EPUB file", type=["epub"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as temp_epub:
        temp_epub.write(uploaded_file.read())
        epub_path = temp_epub.name

    txt_path = epub_path.replace(".epub", ".txt")
    pdf_path = epub_path.replace(".epub", ".pdf")

    try:
        st.info("Converting EPUB → HTML (via Pandoc)...")
        html_path = epub_path.replace(".epub", ".html")
        pypandoc.convert_file(epub_path, 'html', outputfile=html_path)

        st.info("Extracting text...")
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator="\n")

        st.info("Generating PDF (text-only)...")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in text.split("\n"):
            pdf.multi_cell(0, 10, line)

        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        st.success("✅ Conversion successful! (text-only formatting)")

    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")

    finally:
        for path in [epub_path, txt_path, pdf_path, html_path]:
            if os.path.exists(path):
                os.remove(path)
