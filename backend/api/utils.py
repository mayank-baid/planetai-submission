import fitz
async def extract_text_from_pdf(filepath):
    text = ''
    try:
        with fitz.open(filepath) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text


