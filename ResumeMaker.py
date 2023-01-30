from docx import Document
from docx2pdf import convert
import streamlit as st
import os
import pdfkit
import docx
from openAI import CallAI
from pathlib import Path
import streamlit as st
import requests

current_dir = Path(__file__).parent

#Object to call AI to rephrase the text input
AI = CallAI()

class CreateResume:
    def create_resume(self,template_file, data):
        # Open the template file
        doc = Document(template_file)

        # Define mapping of template placeholder and data key
        mapping = {
            "{{Name}}": "Name",
            "{{Objective}}": "Objective",
            "{{Address}}": "Address",
            "{{Phone}}": "Phone",
            "{{Email}}": "Email",
            "{{JOBTITLE}}": "JOBTITLE",
            "{{COMPANY}}": "COMPANY",
            "{{ExpPlace}}": "ExpPlace",
            "{{ExpDuration}}": "ExpDuration",
            "{{job description}}": "job description",
            "{{Technical Skills}}": "Technical Skills",
            "{{SSkills}}": "SSkills",
            "{{College}}": "College",
            "{{Degree}}": "Degree",
            "{{CollegePlace}}": "CollegePlace",
            "{{CGPA}}": "CGPA",
            "{{CollegeDetails}}": "CollegeDetails",
            "{{CollegeDuration}}": "CollegeDuration",
            "{{Achieve}}": "Achievement"
        }
        
        # Iterate through the document's paragraphs and replace placeholders
        for para in doc.paragraphs:
            for run in para.runs:
                for key, value in mapping.items():
                    if key in run.text:
                        run.text = run.text.replace(key, data[value])
                        
        # Save the document with a new file name
        doc.save(current_dir /  str('Output/'+data['Name']+'_Resume.docx'))

    # Convert to pdf
    def convert_docx_to_pdf(self, docx_file, pdf_file):
        doc = docx.Document(docx_file)
        pdfkit.from_string(doc.text, pdf_file)




data = {
    "Name": "",
    "Objective": "",
    "Address": "",
    "Phone": "",
    "Email": "",
    "JOBTITLE": "",
    "COMPANY": "",
    "ExpPlace": "",
    "ExpDuration": "",
    "job description": "",
    "Technical Skills": "",
    "SSkills": "",
    "College": "",
    "Degree": "",
    "CollegePlace": "",
    "CGPA": "",
    "CollegeDetails": "",
    "CollegeDuration": "",
    "Achievement": ""
}



st.title("Resume Generator")
options = ["Basic Details", "Experience", "Academic info"]
selected_option = st.selectbox("Select Category", options)
# Get user inputs
data = {}
if selected_option == "Basic Details":
    data["Name"] = st.text_input("Enter your name:")
    data["Address"] = st.text_input("Enter your address:")
    data["Phone"] = st.text_input("Enter your phone number:")
    data["Email"] = st.text_input("Enter your email:")

if selected_option == "Experience":
    data["JOBTITLE"] = st.text_input("Enter your job title:")
    data["COMPANY"] = st.text_input("Enter your company name:")
    data["ExpPlace"] = st.text_input("Enter your experience place:")
    data["ExpDuration"] = st.text_input("Enter your experience duration:")
    try:
        data["Objective"] = AI.getAI('Rephrase following to add in resume summary section in full sentance : '+st.text_input("Enter your Career objective (Rephrase using AI):"))
        data["job description"] = AI.getAI('Rephrase following to add in Resume experience in bulletin points : '+st.text_input("Enter your job description (Rephrase using AI):"))
    except:
        data["Objective"] = st.text_input("Enter your Career objective:")
        data["job description"] = st.text_input("Enter your job description:")
data["Technical Skills"] = st.text_input("Enter your technical skills:")
data["SSkills"] = st.text_input("Enter your soft skills:")

if selected_option == "Academic info":
    data["College"] = st.text_input("Enter your college name:")
    data["Degree"] = st.text_input("Enter your degree:")
    data["CollegePlace"] = st.text_input("Enter your college place:")
    data["CGPA"] = st.text_input("Enter your CGPA:")
    data["CollegeDetails"] = st.text_input("Enter your college details:")
    data["CollegeDuration"] = st.text_input("Enter your college duration:")
data["Achievement"] = st.text_input("Enter your achievements:")

template_file = current_dir/ "resume_template.docx"



if st.button('Generate Resume'):
    resume = CreateResume()
    resume.create_resume(template_file, data)
    #resume.convert_docx_to_pdf('Ajmal.docx', "output.pdf")

    resume_file = current_dir /  str('Output/'+data['Name']+'_Resume.docx')
    with open(resume_file, "rb") as word_file:
        word_byte = word_file.read()
    st.download_button(
        label=" 📄 Download Word Document",
        data=word_byte,
        file_name=resume_file.name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
