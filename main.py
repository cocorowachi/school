import streamlit as st
import pypandoc
import tempfile
import os
from xhtml2pdf import pisa

st.set_page_config(page_title="EPUB → PDF Converter", page_icon="📚")

st.title("📚 EPUB to PDF Converter")
st.write("Upload an EPUB file and convert it to a PDF while keeping formatting, images, and styles.")

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

        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        st.info("Rendering HTML → PDF with xhtml2pdf...")
        with open(pdf_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

        if pisa_status.err:
            st.error("❌ PDF generation failed. Some advanced CSS may not be supported.")
        else:
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Styled PDF",
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
