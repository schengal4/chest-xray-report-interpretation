import streamlit as st
from openai import OpenAI
import json
from utils import upload_file, text_from_pdf_file_path, json_to_table, clarify_findings
import pandas as pd

# @st.cache_data
def classify_xray(report, test=False):
    client = OpenAI()
    system = """
    You are a helpful chatbot, that can accurately classify radiology reports for the presence or absence of findings. 
    Each report, you will classify for the presence or absence of the following findings: 
    Cardiac congestion, lung opacities (that includes pneumonia, atelectasis, dystelectasis and other airway processes), 
    pleural effusion (this does NOT include pericardial effusion), pneumothorax, presence of thoracic drains, 
    presence of venous catheters, presence of gastric tubes, presence of tracheal tubes, misplacement of any devices. 
    structure your answer like the template I provide you and return this template
    {
        "congestion": "[0/1]",
        "opacity": "[0/1]",
        "effusion": "[0/1]",
        "pneumothorax": "[0/1]",
        "thoracic_drain": "[0/1]",
        "venous_catheter": "[0/1]",
        "gastric_tube": "[0/1]",
        "tracheal_tube": "[0/1]",
        "misplaced": "[0/1]",
    }
    """
    if test:
        model = "gpt-3.5-turbo"
    else:
        model = "gpt-4"
    response = client.chat.completions.create(model=model,
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": report},
    ])
    result = response.choices[0].message.content
    json_text = result.split("{", 1)[1].split("}", 1)[0]
    return json.loads("{" + json_text + "}")
def initialize_session_state():
     if "interpreted_report" not in st.session_state:
        st.session_state["interpreted_report"] = None

def instructions():
    st.write("This tool is designed to help radiologists identify pathologies and medical devices in chest X-ray reports. \
             To this end, it uses the OpenAI API (GPT-4).")
    st.write("### Instructions")
    st.write("""
              1. Upload a chest X-ray report as a .txt, .pdf, or .docx file. Or, enter/paste the report into the text box and press Ctrl+Enter.
              2. Click the 'Submit' button.  
              3. After ~10 seconds, the report will be structured and displayed below in a table format.  
             
            To try an example, click the 'Try example' button. After ~10 seconds, the \
            findings will be displayed below.
             """)
def credits():
    st.write("### Credits")
    st.write("This app is a Streamlit adaptation of the xray-clf.py file in the [gpt4-structured-reporting](https://github.com/kbressem/gpt4-structured-reporting) GitHub repository, \
             created by Keno Bressem, a board-certified radiologist. For more information about him, please \
             see https://aim.hms.harvard.edu/team/keno-bressem.")
    st.write("The core functionality/prompts used are based on the paper [Leveraging GPT-4 for Post Hoc Transformation of Free-text Radiology Reports into Structured Reporting: A Multilingual Feasibility Study](https://doi.org/10.1148/radiol.230725), published in April 2023 and cited by 51+ different papers so far. ")
def disclaimer():
    st.markdown("### Disclaimer")
    st.write("This app is for educational and research use only, and it cannot replace clinical judgment. Don't upload patient information or any other sensitive information to a third party API.")

def highlight_table_row(row):
    return ['background-color: green; color: white']*len(row) if row["Presence/Absence of Findings"] == "Absent" else ['background-color: red; color:white']*len(row)

def process_xray_report(report):
    progress_msg = st.empty()
    progress_msg.info("Processing the report. This will likely take ~10 seconds.")
    st.session_state["interpreted_report"] = classify_xray(report, test=False)
    progress_msg.empty()
def main():
    initialize_session_state()
    st.title("Chest X-Ray Interpretation")
    instructions()
    # Upload a file or enter/paste a report
    st.markdown("### Upload or enter/paste chest X-ray report")
    FILE_UPLOAD_OPTIONS = ["Upload report as file", "Paste report"]
    EXAMPLE_FILE_PATH = "example_files/sample_chest_xray_report.pdf"
    upload_option = st.radio("Upload a file or paste a report", (FILE_UPLOAD_OPTIONS[0], FILE_UPLOAD_OPTIONS[1]), horizontal=True)
    if upload_option == FILE_UPLOAD_OPTIONS[0]:
        report = upload_file()
    elif upload_option == FILE_UPLOAD_OPTIONS[1]:
        text_container = st.empty()
        report = text_container.text_area("Paste your report here")
    
    col1, col2, _ = st.columns([1, 2, 4])
    submit = col1.button("Submit", key="submit", help="Submit the report for processing", type="primary")
    try_example = col2.button("Try an example", key="try_example", help="Try an example report. This report is from https://usarad.com/pdf/xray/cr_chest.pdf.")

    # If the user hasn't submitted a report, don't send it to OpenAI API.
    if not st.session_state["interpreted_report"] and not try_example and (not report or not report.strip()):
        disclaimer()
        credits()
        st.stop()

    # Code for handling when an user clicks the "Try an example" button
    if try_example:
        if upload_option == FILE_UPLOAD_OPTIONS[1]:

            # Example comes from https://usarad.com/pdf/xray/cr_chest.pdf 
            EXAMPLE_REPORT_TEXT = """
            Patient: DOE, JOHN (M)
            Referring Physician: XMRI, SECOND OPINION
            MRN : JD1004 DOB: 07/08/1987
            Exam Date: 12/27/2013
            FAX: 888-886-2486
            CLINICAL HISTORY: Cough, congestion.
            COMMENTS:
            PA and lateral views of chest reveals no evidence of active pleural or pulmonary parenchymal
            abnormality.
            There are diffusely increased interstitial lung markings consistent with chronic bronchitis. Underlying
            pulmonary fibrosis is not excluded.
            The cardiac silhouette is enlarged. The mediastinum and pulmonary vessels appear normal. Aorta is
            tortuous.
            Degenerative changes are noted in the thoracic spine.
            IMPRESSION:
            1. No evidence of acute pulmonary pathology.
            2. Enlarged cardiac silhouette.
            3. Tortuous aorta.
            4. Diffusely increased interstitial lung markings consistent with chronic bronchitis. Underlying
            pulmonary fibrosis is not excluded.
            5. Consider follow up with Chest CT if clinically warranted.
            -Electronically Signed by: MICHAEL YUZ, M.D., CERTIFIED BY ABR & CBCCT on
            CR OF THE CHEST TWO VIEWS
            12/30/2013 11:12:08 AM
            """
            report = text_container.text_area("Report", value=EXAMPLE_REPORT_TEXT, height=400, max_chars=10000) 
        elif upload_option == FILE_UPLOAD_OPTIONS[0]:
            report = text_from_pdf_file_path(EXAMPLE_FILE_PATH)
        process_xray_report(report)
    # Code for handling when an user clicks the "Submit" button
    if submit and report.strip():
        process_xray_report(report)
    # Display the findings.
    if st.session_state["interpreted_report"]:
        st.markdown("### Please review the findings below:")
        interpreted_report = st.session_state["interpreted_report"]
        clarified_findings = clarify_findings(interpreted_report)
        st.dataframe(clarified_findings.style.apply(highlight_table_row, axis=1))
        st.write("##### Terminology Definitions:")
        st.write("""
                    - **Cardiac congestion**: Presence of excess fluid in lungs due to heart's failure to pump blood effectively.  
                    - **Lung opacities**: Gray hazy/cloudy areas on the chest X-ray. This can indicate a variety of conditions including pneumonia, tumors, or other diseases.  
                    - **Pleural effusion**: Accumulation of fluid in the space between the layers of the pleura outside the lungs.  
                    - **Pneumothorax**: Presence of air or gas in the cavity between the lung and the chest wall, causing the lung to collapse.  
                    - **Thoracic drain**: A tube inserted into the chest (pleural space) to drain air, blood, or fluid. 
                    - **Venous catheter**: A long, flexible tube that healthcare professionals insert into a vein in the arm, chest, neck, or groin. It can stay in place for a while if needed.  
                    - **Gastrostomy tube**: A tube that's placed through the nose or mouth and goes down to the stomach. It's used to feed someone who can't eat by mouth, give medicine, or to remove stomach contents.  
                    - **Tracheal tube**: A flexible tube that doctors put into a person's windpipe through the mouth or nose. It's often used when someone has difficulty breathing on their own, to make sure air can get in and out of the lungs.  
                    - **Misplacement of devices**: This indicates whether any medical devices, such as pacemakers or defibrillators, are not in their correct position.  
                 """)
    disclaimer()
    credits()
if __name__ == "__main__":
    main()