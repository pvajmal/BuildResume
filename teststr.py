import streamlit as st

experiences = []


title = st.text_input("Title")
company = st.text_input("Company")
duration = st.text_input("Duration")
description = st.text_area("Description")

if st.button("Add Experience"):
    experiences.append({"title": title, "company": company, "duration": duration, "description": description})

st.write(experiences)