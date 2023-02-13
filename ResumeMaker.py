import os
import json
import streamlit as st
import docx
import pdfkit
from pathlib import Path
from openAI import CallAI
import re
import datetime
from gtts import gTTS
import datetime
from IPython.display import Audio
import reportlab
from reportlab.pdfgen import canvas
from jinja2 import Template


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

def html_to_pdf(data):
    # Load the template
    with open("template.html", "r") as file:
        template = Template(file.read())

    # Render the template with the sample input data
    html = template.render(data=data)

    # Write the HTML code to a file
    with open("resume.html", "w") as file:
        file.write(html)

    # Create a canvas object to generate the PDF
    c = canvas.Canvas("resume.pdf")

    # Load the HTML file and draw it on the canvas
    c.drawString(72, 720, html)

    # Save the PDF
    c.save()

    try:
        wkhtml_path = pdfkit.configuration(wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")  #by using configuration you can add path value.
        pdfkit.from_file("resume.html", "resume.pdf", configuration= wkhtml_path)
    except:
        pdfkit.from_file("resume.html", "resume.pdf")
    #pdfkit.from_url('https://stackoverflow.com/questions/33705368/unable-to-find-wkhtmltopdf-on-this-system-the-report-will-be-shown-in-html', 'C:/Users/Admin/Desktop/Trial1.pdf', configuration = wkhtml_path)

def main():
    resume = CreateResume()
    data = resume.load_data()
    st.set_page_config(page_icon="📑", page_title="Resume Generator")
    options = ["Basic Details", "Experience", "Academic Info", "Skills, Achievements etc.","Ask AI", "Day Difference Calculator"]
    selected_option = st.sidebar.selectbox("Select Category", options)

    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email)
    # Get user inputs
    if selected_option == "Basic Details":
        resume.data["Name"] = st.text_input("Enter your name:")
        resume.data["Address"] = st.text_input("Enter your address:")
        resume.data["Phone"] = st.text_input("Enter your phone number:")
        email = st.text_input("Enter your email:")
        if is_valid_email(email):
            resume.data["Email"] = email
        else:
            st.error("Invalid email address. Please try again.")
        resume.data["LinkedIn"] = st.text_input("Enter your LinkedIn ID:")
        resume.data["Objective"] = st.text_area("Enter your Career objective:")
        call_ai_basic = st.button("Use AI to write career objecive based on your input")
        if call_ai_basic:
             resume.data["Objective"] = AI.getAI("Please craft a compelling and relevant career objective using the following information: "+ resume.data["Objective"])
             st.write(resume.data["Objective"])
        st.write("")
    elif selected_option == "Ask AI":
        def tts(text):
            tts = gTTS(text)
            tts.save("tts.mp3")
            return Audio("tts.mp3", autoplay=True)
        
        Q_AI = st.text_area("Ask me a question!")
        call_ai_q = st.button("ASK")
        if call_ai_q:
            AI_response = AI.getAI("answer following question "+ Q_AI)
            st.write(tts(AI_response))
            st.write(AI_response)
    elif selected_option == "Experience":            
        if "experiences" not in resume.data:
            resume.data["experiences"] = []
        title = st.text_input("Title")
        company = st.text_input("Company")
        start_date = st.date_input("Start Date", value=datetime.datetime.now())
        end_date = st.date_input("End Date", value=datetime.datetime.now())
        description = st.text_area("Description")
        call_ai_exp = st.button("Use AI to write job responsibilites based on your input")
        if call_ai_exp:
            description = (AI.getAI("write standard job responsibilities in asteric points to add in resume using" +description))
            st.write(description)
        buttons = st.empty()
        add_exp_button = st.button("Add Experience")
        clear_exp_button = st.button("Clear Experience")

        if add_exp_button:
            resume.data["experiences"].append({"title": title, "company": company, "duration": str(start_date.strftime('%b %Y'))+ " - "+ str(end_date.strftime('%b %Y')), "description": description})

        if clear_exp_button:
            resume.data["experiences"].clear()

        st.write("Current Experiences:")
        i = 1
        for exp in resume.data["experiences"]:
            st.write(f"Experience {i}:")
            st.write(f"Title: {exp['title']}")
            st.write(f"Company: {exp['company']}")
            st.write(f"Duration: {start_date.strftime('%b %Y')} - {end_date.strftime('%b %Y')}")
            st.write(f"Description: {exp['description']}")
            st.write("")
            i += 1
    
    elif selected_option == "Skills, Achievements etc.":
        resume.data["Skills"] = st.text_input("Enter your skills:")
        if "achievements" not in resume.data:
            resume.data["achievements"] = []
        
        i = len(resume.data["achievements"])
        while True:
            st.write("Achievement #", len(resume.data["achievements"]) + 1)
            dateAchievement = st.date_input("Enter the date:", key=f'dateAchievement_{i}')
            placeAchievement = st.text_input("Enter the place:", key=f'placeAchievement_{i}')
            descriptionAchievement = st.text_area("Enter a description:", key=f'descriptionAchievement_{i}')

            add_achievement = st.button("Add", key=f"add_achievement_{i}")
            if add_achievement:
                resume.data["achievements"].append({"date": dateAchievement.strftime('%b %Y'), "place":placeAchievement, "description": descriptionAchievement})

            remove_achievement = st.button("Remove",  key=f"remove_achievement_{i}")
            if remove_achievement and len(resume.data["achievements"])>=1:
                resume.data["achievements"].pop()
                i -= 1
            if not add_achievement:
                break

            i += 1
        
        

        if "certifications" not in resume.data:
            resume.data["certifications"] = []
        j = 0
        while True:
            st.write("Certification #", len(resume.data["certifications"]) + 1)
            dateCertification = st.date_input("Enter the date:", key=f'dateCertification_{j}')
            placeCertification = st.text_input("Enter the place:", key=f'placeCertification_{j}')
            descriptionCertification = st.text_area("Enter a description:", key=f'descriptionCertification_{j}')

            add_certification = st.button("Add", key=f"add_certification_{j}")
            if add_certification:
                resume.data['certifications'].append({"date": dateCertification.strftime('%b %Y'), "place":placeCertification, "description": descriptionCertification})

            remove_certification = st.button("Remove",  key=f"remove_certification_{j}")
            if remove_certification and len(resume.data['certifications']) >= 0:
                resume.data['certifications'].pop()
            
            if not add_certification:
                break

            j += 1

        

    elif selected_option == "Academic Info":
        if "education" not in resume.data:
            resume.data["education"] = []

        school = st.text_input("School Name")
        degree = st.text_input("Degree")
        start_date = st.date_input("Start Date", value=datetime.datetime.now())
        end_date = st.date_input("End Date", value=datetime.datetime.now())
        city = st.text_input("City")
        score = st.text_input("CGPA/Percentage")

        buttons = st.empty()
        add_edu_button = st.button("Add Education")
        clear_edu_button = st.button("Clear Education")

        if add_edu_button:
            resume.data["education"].append({"school": school, "degree": degree, "start_date": str(start_date.strftime('%b %Y')), "end_date": str(end_date.strftime('%b %Y')), "city": city, "score": score})

        if clear_edu_button:
            resume.data["education"].clear()

        st.write("Current Education:")
        i = 1
        for edu in resume.data["education"]:
            st.write(f"Education {i}:")
            st.write(f"School: {edu['school']}")
            st.write(f"Degree: {edu['degree']}")
            st.write(f"Start Date: {start_date.strftime('%b %Y')}")
            st.write(f"End Date: {end_date.strftime('%b %Y')}")
            st.write(f"City: {edu['city']}")
            st.write(f"CGPA/Percentage: {edu['score']}")
            st.write("")
            i += 1
    elif selected_option == "Day Difference Calculator":
        start_date = st.date_input("Start Date", value=datetime.datetime.now())
        end_date = st.date_input("End Date", value=datetime.datetime.now())
        calc_diff = st.button("Calculate Difference of days")
        if calc_diff:
            dayDiff = end_date - start_date
            st.write(f"Difference between {start_date} and {end_date} is: {dayDiff.days} day(s).")



    if st.button("Generate Resume"):
        # Generate the resume in PDF format
        
        html_to_pdf(data)
        pdf_file =  current_dir / "resume.pdf"
        with open(pdf_file, "rb") as pdf_file_handle:
            pdf_byte = pdf_file_handle.read()
        st.download_button(
            label=" 📄 Download pdf Document",
            data=pdf_byte,
            file_name=pdf_file.name,
            mime="application/pdf",
        )

    if st.button("Clear Data"):
        # Clear the stored data
        resume.data.clear()

        # Show success message
        st.success("All details entered are now cleared from the database. Please start entering details again.")

    # Save the data
    resume.save_data()


if __name__ == "__main__":
    main()
