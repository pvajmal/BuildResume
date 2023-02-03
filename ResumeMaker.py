import os
import json
import streamlit as st
import docx
import pdfkit
from pathlib import Path
from DocxTemplate import ResumeTemplate
from openAI import CallAI

template = ResumeTemplate()
AI = CallAI()

current_dir = Path(__file__).parent
class CreateResume:
    def __init__(self):
        self.data = self.load_data()
    
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
    data = resume.load_data()
    st.set_page_config(page_icon="📑", page_title="Resume Generator")
    options = ["Basic Details", "Experience", "Academic Info", "Skills & Achievements","Ask AI!"]
    selected_option = st.radio("Select Category", options)


    # Get user inputs
    if selected_option == "Basic Details":
        resume.data["Name"] = st.text_input("Enter your name:")
        resume.data["Address"] = st.text_input("Enter your address:")
        resume.data["Phone"] = st.text_input("Enter your phone number:")
        resume.data["Email"] = st.text_input("Enter your email:")
        resume.data["LinkedIn"] = st.text_input("Enter your LinkedIn ID:")
        resume.data["Objective"] = st.text_area("Enter your Career objective:")
        call_ai_basic = st.button("Use AI to write career objecive")
        if call_ai_basic:
             resume.data["Objective"] = AI.getAI("Write an awesome resume career objective using "+ resume.data["Objective"])
             st.write(resume.data["Objective"])
        st.write("")
    elif selected_option == "Ask AI!":
        Q_AI = st.text_area("Ask me question!")
        call_ai_q = st.button("ASK")
        if call_ai_q:
            st.write(AI.getAI("answer following question "+ Q_AI))
    elif selected_option == "Experience":
        
        if "experiences" not in resume.data:
            resume.data["experiences"] = []
        title = st.text_input("Title")
        company = st.text_input("Company")
        duration = st.text_input("Duration")
        description = st.text_area("Description")
        call_ai_exp = st.button("Use AI to write job responsibilites")
        if call_ai_exp:
             description = (AI.getAI("Convert following to add in resume (job responsibilities)" +description))
             st.write(description)
        buttons = st.empty()
        add_exp_button = st.button("Add Experience")
        clear_exp_button = st.button("Clear Experience")


        if add_exp_button:
            resume.data["experiences"].append({"title": title, "company": company, "duration": duration, "description": description})

        if clear_exp_button:
            resume.data["experiences"].clear()

        st.write("Current Experiences:")
        i = 1
        for exp in resume.data["experiences"]:
            st.write(f"Experience {i}:")
            st.write(f"Title: {exp['title']}")
            st.write(f"Company: {exp['company']}")
            st.write(f"Duration: {exp['duration']}")
            st.write(f"Description: {exp['description']}")
            st.write("")
            i += 1
        
    elif selected_option == "Skills & Achievements":
        resume.data["Skills"] = st.text_input("Enter your skills:")
        call_ai_skill = st.button("Use AI to write skills")
        if call_ai_skill:
             resume.data["Skills"]  = (AI.getAI("convert following to add in resume skills section. I need to add in bulletin points"+ resume.data["Skills"] ))
             st.write(resume.data["Skills"])
        resume.data["Achievement"] = st.text_area("Enter your achievements:")
    elif selected_option == "Academic Info":
        if "education" not in resume.data:
            resume.data["education"] = []

        school = st.text_input("School Name")
        degree = st.text_input("Degree")
        start_date = st.text_input("Start Date")
        end_date = st.text_input("End Date")
        city = st.text_input("City")
        description = st.text_area("Description")

        buttons = st.empty()
        add_edu_button = st.button("Add Education")
        clear_edu_button = st.button("Clear Education")

        if add_edu_button:
            resume.data["education"].append({"school": school, "degree": degree, "start_date": start_date, "end_date": end_date, "city": city, "description": description})

        if clear_edu_button:
            resume.data["education"].clear()

        st.write("Current Education:")
        i = 1
        for edu in resume.data["education"]:
            st.write(f"Education {i}:")
            st.write(f"School: {edu['school']}")
            st.write(f"Degree: {edu['degree']}")
            st.write(f"Start Date: {edu['start_date']}")
            st.write(f"End Date: {edu['end_date']}")
            st.write(f"City: {edu['city']}")
            st.write(f"Description: {edu['description']}")
            st.write("")
            i += 1


    if st.button('Generate Resume'):
        try:
            document = template.CreateResume(data)
            # Save the document
            document.save(current_dir /str('output/' + data['Name'] + '_Resume.docx'))
            st.success("Resume generated successfully!")
            pdf_file =  current_dir / os.path.join("output", f"{resume.data['Name']}_Resume.pdf")
            resume_file = current_dir / str('output/' + resume.data['Name'] + '_Resume.docx')
            with open(resume_file, "rb") as word_file:
                word_byte = word_file.read()
            st.download_button(
                label=" 📄 Download Word Document",
                data=word_byte,
                file_name=resume_file.name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        except:
            st.write("You need to go through all categories to create your resume!")
    if st.button('Clear Data'):
         resume.data.clear()
         st.write("All details entered is now cleared from database! Please start to enter details.")
    resume.save_data()

if __name__ == "__main__":
    main()
