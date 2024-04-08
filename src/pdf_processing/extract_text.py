import fitz
def extract_text_from_pdf(buffer):
    doc = fitz.open("pdf", buffer)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
