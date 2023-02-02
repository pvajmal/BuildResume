
import streamlit as st
from openAI import CallAI
from pathlib import Path
import streamlit as st
from create_resume import CreateResume


current_dir = Path(__file__).parent

# Object to call AI to rephrase the text input
AI = CallAI()




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
        resume_file = current_dir / str('Output/' + data['Name'] + '_Resume.docx')
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
