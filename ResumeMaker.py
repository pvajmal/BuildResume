import os
import json
import streamlit as st
import docx
import pdfkit
from pathlib import Path

current_dir = Path(__file__).parent
class CreateResume:
    def __init__(self):
        self.mapping = {
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
            "{{LinkedIn}}" : "LinkedIn",
            "{{College}}": "College",
            "{{Degree}}": "Degree",
            "{{CollegePlace}}": "CollegePlace",
            "{{CGPA}}": "CGPA",
            "{{CollegeDetails}}": "CollegeDetails",
            "{{CollegeDuration}}": "CollegeDuration",
            "{{Achieve}}": "Achievement"
        }
        self.data = self.load_data()
    
    def create_resume(self, template_file):
        doc = docx.Document(template_file)

        for para in doc.paragraphs:
            for run in para.runs:
                for key, value in self.mapping.items():
                    if key in run.text:
                        run.text = run.text.replace(key, self.data.get(value, ''))

        os.makedirs('output', exist_ok=True)
        file_path = os.path.join('output', f"{self.data['Name']}_Resume.docx")
        doc.save(file_path)

    def convert_docx_to_pdf(self, docx_file, pdf_file):
        doc = docx.Document(docx_file)
        pdfkit.from_string(doc.text, pdf_file)

    def save_data(self):
        with open("data.json", "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        try:
            with open("data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

def main():
    resume = CreateResume()
    st.title("Resume Generator")
    options = ["Basic Details", "Experience", "Academic info", "Skills and Achievements"]
    selected_option = st.radio("Select Category", options)

    # Get user inputs
    if selected_option == "Basic Details":
        resume.data["Name"] = st.text_input("Enter your name:")
        resume.data["Address"] = st.text_input("Enter your address:")
        resume.data["Phone"] = st.text_input("Enter your phone number:")
        resume.data["Email"] = st.text_input("Enter your email:")
        resume.data["LinkedIn"] = st.text_input("Enter your LinkedIn ID:")
    elif selected_option == "Experience":
        resume.data["JOBTITLE"] = st.text_input("Enter your job title:")
        resume.data["COMPANY"] = st.text_input("Enter your company name:")
        resume.data["ExpPlace"] = st.text_input("Enter your experience place:")
        resume.data["ExpDuration"] = st.text_input("Enter your experience duration:")
        resume.data["Objective"] = st.text_input("Enter your Career objective:")
        resume.data["job description"] = st.text_input("Enter your job description:")
    elif selected_option == "Skills and Achievements":
        resume.data["Technical Skills"] = st.text_input("Enter your technical skills:")
        resume.data["SSkills"] = st.text_input("Enter your soft skills:")
        resume.data["Achievement"] = st.text_input("Enter your achievements:")
    elif selected_option == "Academic info":
        resume.data["College"] = st.text_input("Enter your college name:")
        resume.data["Degree"] = st.text_input("Enter your degree:")
        resume.data["CollegePlace"] = st.text_input("Enter your college place:")
        resume.data["CGPA"] = st.text_input("Enter your CGPA:")
        resume.data["CollegeDetails"] = st.text_input("Enter your college details:")
        resume.data["CollegeDuration"] = st.text_input("Enter your college duration:")

    if st.button('Generate Resume'):
        template_file = current_dir / "resume_template.docx"
        resume.create_resume(template_file)
        st.success("Resume generated successfully!")
        pdf_file = os.path.join("output", f"{resume.data['Name']}_Resume.pdf")
        if st.button("Download PDF"):
            resume.convert_docx_to_pdf(file_path, pdf_file)
            with open(pdf_file, "rb") as f:
                st.write(f.read(), unsafe_allow_html=True)
    resume.save_data()

if __name__ == "__main__":

    main()
