from docx import Document
import streamlit as st
from openAI import CallAI
from pathlib import Path
import json

current_dir = Path(__file__).parent
css_file = current_dir / "styles" / "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
# Object to call AI to rephrase the text input
AI = CallAI()



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
            "{{LinkedIn}}" : "LinkedIn",
            "{{College}}": "College",
            "{{Degree}}": "Degree",
            "{{CollegePlace}}": "CollegePlace",
            "{{CGPA}}": "CGPA",
            "{{CollegeDetails}}": "CollegeDetails",
            "{{CollegeDuration}}": "CollegeDuration",
            "{{Achieve}}": "Achievement"
        }


        # Iterate through the document's paragraphs
        for para in doc.paragraphs:
            for run in para.runs:
                for key, value in mapping.items():
                    if key in run.text:

                        run.text = run.text.replace(key, data.get(value, ''))

        # Save the document with a new file name
        if not os.path.exists('output'):
            os.mkdir('output')
        file_path = os.path.join('output', f"{data['Name']}_Resume.docx")
        doc.save(file_path)


    # Convert to pdf
    def convert_docx_to_pdf(self, docx_file, pdf_file):
        doc = docx.Document(docx_file)
        pdfkit.from_string(doc.text, pdf_file)





def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def main():
    resume = CreateResume()
    data = resume.load_data()
    st.title("Resume Generator")
    options = ["Basic Details", "Experience", "Academic info", "Skills and Achievements"]
    selected_option = st.radio("Select Category", options)

    # Get user inputs
    if selected_option == "Basic Details":
        data["Name"] = st.text_input("Enter your name:")
        data["Address"] = st.text_input("Enter your address:")
        data["Phone"] = st.text_input("Enter your phone number:")
        data["Email"] = st.text_input("Enter your email:")
        data["LinkedIn"] = st.text_input("Enter your LinkedIn ID:")
        resume.save_data(data)
    elif selected_option == "Experience":
        data["JOBTITLE"] = st.text_input("Enter your job title:")
        data["COMPANY"] = st.text_input("Enter your company name:")
        data["ExpPlace"] = st.text_input("Enter your experience place:")
        data["ExpDuration"] = st.text_input("Enter your experience duration:")
        data["Objective"] = st.text_input("Enter your Career objective:")
        data["job description"] = st.text_input("Enter your job description:")
        resume.save_data(data)
    elif selected_option == "Skills and Achievements":
        data["Technical Skills"] = st.text_input("Enter your technical skills:")
        data["SSkills"] = st.text_input("Enter your soft skills:")
        data["Achievement"] = st.text_input("Enter your achievements:")
        resume.save_data(data)
    elif selected_option == "Academic info":
        data["College"] = st.text_input("Enter your college name:")
        data["Degree"] = st.text_input("Enter your degree:")
        data["CollegePlace"] = st.text_input("Enter your college place:")
        data["CGPA"] = st.text_input("Enter your CGPA:")
        data["CollegeDetails"] = st.text_input("Enter your college details:")
        data["CollegeDuration"] = st.text_input("Enter your college duration:")
        resume.save_data(data)

    template_file = current_dir / "resume_template.docx"

    if st.button('Generate Resume'):
        
        resume.create_resume(template_file, data)
        resume_file = current_dir / str('output/' + data['Name'] + '_Resume.docx')
        with open(resume_file, "rb") as word_file:
            word_byte = word_file.read()
        st.download_button(
            label=" 📄 Download Word Document",
            data=word_byte,
            file_name=resume_file.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

if __name__ == "__main__":

    main()
