
from docx import Document
import fitz # Here's the link to the license of the library: https://www.gnu.org/licenses/agpl-3.0.html
from io import BytesIO
import pandas as pd
import json
import streamlit as st

def read_docx(file):
    with BytesIO(file.read()) as doc_file:
        document = Document(doc_file)
        result = "\n".join([para.text for para in document.paragraphs])
        return result
def text_from_pdf_file(pdf_file):
    # Limitations:  Only works for PDFs with text, not images.
    # Can't properly processing footers and headers.
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text

def text_from_pdf_file_path(pdf_file_path):
    # Limitations: Only works for PDFs with text, not scanned images.
    # Might not properly process footers and headers.
    with fitz.open(pdf_file_path) as doc:  # Use the file path directly
        report_text = ""
        for page in doc:
            report_text += page.get_text()
    return report_text
# Convert json object to a pandas DataFrame
def json_to_table(json_obj_):
    def flatten_json(y, prefix=''):
        out = {}
        for key in y:
            if isinstance(y[key], dict):
                out.update(flatten_json(y[key], prefix + key + ': '))
            elif isinstance(y[key], list):
                for i, item in enumerate(y[key]):
                    if isinstance(item, dict):
                        out.update(flatten_json(item, prefix + key + ': ' + str(i) + ': '))
                    else:
                        out[prefix + key + ': ' + str(i)] = item
            else:
                out[prefix + key] = y[key]
        return out

    flat_report = flatten_json(json_obj_)
    df = pd.DataFrame([flat_report])
    df = df.T
    return df