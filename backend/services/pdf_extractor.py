import fitz
from backend.utils.text_cleaner import clean_extracted_text

async def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.Document(stream=file_bytes, filetype='pdf')
    text = ""
    for page in doc:
        text += page.get_text()
    return clean_extracted_text(text)