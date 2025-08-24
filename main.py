import streamlit as st
import pypandoc
from fpdf import FPDF
from bs4 import BeautifulSoup
import tempfile
import os

st.set_page_config(page_title="EPUB → PDF Converter", page_icon="📚")

st.title("📚 EPUB to PDF Converter")
st.write("Upload an EPUB file and convert it to a PDF (text-only, no LaTeX/WeasyPrint).")

uploaded_file = st.file_uploader("Choose an EPUB file", type=["epub"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as temp_epub:
        temp_epub.write(uploaded_file.read())
        epub_path = temp_epub.name

    html_path = epub_path.replace(".epub", ".html")
    pdf_path = epub_path.replace(".epub", ".pdf")

    try:
        st.info("Converting EPUB → HTML with Pandoc...")
        pypandoc.convert_file(epub_path, 'html', outputfile=html_path)

        st.info("Extracting text from HTML...")
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.get_text(separator="\n")

        st.info("Generating PDF...")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in text.split("\n"):
            if line.strip():  # skip empty lines
                pdf.multi_cell(0, 10, line)

        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )
        st.success("✅ Conversion successful!")

    except Exception as e:
        st.error(f"❌ Conversion failed: {e}")

    finally:
        for path in [epub_path, html_path, pdf_path]:
            if os.path.exists(path):
                os.remove(path)
