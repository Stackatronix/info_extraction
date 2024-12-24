from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    # """Extract text from a PDF file."""
    
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text