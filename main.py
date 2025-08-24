import streamlit as st
import pypandoc
from fpdf import FPDF
from bs4 import BeautifulSoup
import tempfile
import os
import textwrap

st.set_page_config(page_title="EPUB → PDF Converter", page_icon="📚")

st.title("📚 EPUB to PDF Converter")
st.write("Upload an EPUB file and convert it to a PDF (Unicode + CJK supported).")

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

        st.info("Generating PDF with Unicode font...")
        pdf = FPDF()
        pdf.add_page()

        # ✅ Load Unicode font (fallback to Arial if missing)
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        if os.path.exists(font_path):
            pdf.add_font("DejaVu", "", font_path, uni=True)
            pdf.set_font("DejaVu", size=12)
        else:
            pdf.set_font("Arial", size=12)

        max_width = pdf.w - 2*pdf.l_margin  # usable width

        for line in text.split("\n"):
            if line.strip():
                # ✅ wrap long lines manually to avoid overflow
                wrapped_lines = textwrap.wrap(line, width=80)  # adjust width if needed
                for wl in wrapped_lines:
                    pdf.multi_cell(max_width, 8, wl, align="L")

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
