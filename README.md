# chest-xray-report-interpretation
## Description
The "Chest X-Ray Report Interpretation" app is an innovative application designed to assist radiologists and healthcare professionals in analyzing chest X-ray reports. Utilizing OpenAI's GPT-4 technology, the app interprets textual radiology reports, structuring the findings into a clear, tabulated format. It provides quick assessments of various conditions such as cardiac congestion, lung opacities, and the presence of medical devices, among others.

## Instructions
1. Upload a chest X-ray report as a .txt, .pdf, or .docx file. Or, enter/paste the report into the text box and press Ctrl+Enter.  
2. Click the 'Submit' button.  
3. After ~10 seconds, the report will be structured and displayed below in a table format.

## Credits
This app is a Streamlit adaptation of the xray-clf.py file in the [gpt4-structured-reporting](https://github.com/kbressem/gpt4-structured-reporting) GitHub repository, created by Keno Bressem, a board-certified radiologist. For more information about him, please see https://aim.hms.harvard.edu/team/keno-bressem.

The core functionality/prompts used are based on the paper [Leveraging GPT-4 for Post Hoc Transformation of Free-text Radiology Reports into Structured Reporting: A Multilingual Feasibility Study](https://doi.org/10.1148/radiol.230725), published in April 2023 and cited by 51+ different papers so far.

## Disclaimer
This app is for educational and research use only, and it cannot replace clinical judgment. Don't upload patient information or any other sensitive information to a third party API.
