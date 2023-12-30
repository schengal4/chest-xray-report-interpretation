import streamlit as st

system = """
You are a helpful chatbot, that can accurately classify radiology reports for the presence or absence of findings. 
Each report, you will classify for the presence or absence of the following findings: 
Cardiac congestion, lung opacities (that includes pneumonia, atelectasis, dystelectasis and other airway processes), 
pleural effusion (this does NOT include pericardial effusion), pneumothorax, presence of thoracic drains, 
presence of venous catheters, presence of gastric tubes, presence of tracheal tubes, misplacement of any devices. 
structure your answer like the template I provide you and return this template
{
    "congestion": "[0/1]",
    "opacitiy": "[0/1]",
    "effusion": "[0/1]",
    "pneumothorax": "[0/1]",
    "thoracic_drain": "[0/1]",
    "venous_catheter": "[0/1]",
    "gastric_tube": "[0/1]",
    "tracheal_tube": "[0/1]",
    "misplaced": "[0/1]",
}

"""

def classify_xray(report):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": report},
    ])

    result = response["choices"][0]["message"]["content"]
    json_text = result.split("{", 1)[1].split("}", 1)[0]
    return json.loads("{" + json_text + "}")
