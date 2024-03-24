import fitz

def extract_text_from_pdf(buffer):
    with fitz.open(stream=buffer, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text