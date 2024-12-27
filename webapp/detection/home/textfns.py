from PyPDF2 import PdfReader

# pdf to text
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from .txt file
def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# from docx import Document

# Function to extract text from .docx file
# def extract_text_from_docx(docx_path):
#     doc = Document(docx_path)
#     text = ""
#     for para in doc.paragraphs:
#         text += para.text + '\n'
#     return text

import pandas as pd
def extract_text_from_excel(excel_path):
    # Read the Excel file
    excel_data = pd.read_excel(excel_path, sheet_name=None)  # sheet_name=None reads all sheets
    
    # Concatenate all sheets' data into a single string
    text = ""
    for sheet_name, df in excel_data.items():
        text += f"Sheet: {sheet_name}\n"
        text += df.to_string(index=False) + "\n\n"
    print(text)
    return text