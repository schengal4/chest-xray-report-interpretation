
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
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            report = text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            report = read_docx(uploaded_file)
        elif uploaded_file.type == 'text/plain':
            # Decode the byte content to string
            report = str(uploaded_file.read(), 'utf-8')
        return report
    else:
        return None
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

def clarify_findings(findings):
    """
    Findings: dictionary with keys representing pathologies and values representing the presence/absence of them
    Values interpretation: 0 -> Absent; 1 -> Present

    Returns: a dataframe representing the findings in a more human-readable format

    """
    clarified_findings = dict()
    for finding, value in findings.items():
        if value == '0':
            clarified_findings[finding] = "Absent"
        elif value == '1':
            clarified_findings[finding] = "Present"
        else:
            clarified_findings[finding] = "Unknown"
    table = pd.DataFrame.from_dict(clarified_findings, orient='index', columns=["Presence/Absence of Findings"])
    table.index = ["Cardiac Congestion", "Lung Opacities", "Pleural Effusion", "Pneumothorax", "Thoracic Drain", "Venous Catheter", "Gastrostomy Tube", "Tracheal Tube", "Misplacement of Devices"]
    return table