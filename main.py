import streamlit as st
import pypandoc
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import tempfile
import os

st.set_page_config(page_title="EPUB → PDF Converter", page_icon="📚")

st.title("📚 EPUB to PDF Converter")
st.write("Upload an EPUB file and convert it to a PDF (Unicode + Japanese/Chinese/Korean supported).")

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

        st.info("Extracting text from HTML...")
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        text = soup.get_text(separator="\n")

        st.info("Generating PDF with ReportLab (Unicode safe)...")

        # ✅ Register a Unicode CJK font
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))  # Japanese
        # For Chinese use "STSong-Light", for Korean "HYSMyeongJo-Medium"

        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Custom", fontName="HeiseiMin-W3", fontSize=12, leading=16))

        story = []
        for line in text.split("\n"):
            if line.strip():
                story.append(Paragraph(line.strip(), styles["Custom"]))
                story.append(Spacer(1, 6))

        doc.build(story)

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
