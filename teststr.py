import speech_recognition as sr
import requests
import json
import openai
import streamlit as st 
from gtts import gTTS
from IPython.display import Audio 

def transcribe_audio_file():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Talk")
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio, show_all=True)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        return None

def get_transcription():
    transcription = transcribe_audio_file()
    if transcription:
        return transcription['alternative'][0]['transcript']
    else:
        return None

def get_ai_response(text):
    openai.api_key = "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"
 
    def generate_text(prompt):
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7,
        )

        message = completions.choices[0].text
        return message.strip()

    return generate_text(text)

def tts(text):
    tts = gTTS(text)
    tts.save("tts.mp3")
    return Audio("tts.mp3", autoplay=True)

'''if __name__ == "__main__":
    transcribed_text = get_transcription()
    if transcribed_text:
        print(transcribed_text)
        response_text = get_ai_response(transcribed_text)
        print("Response:", response_text)

        audio = tts(response_text)
        st.write(audio)
    else:
        print("Sorry, I couldn't transcribe your audio.")'''
tts('''LinkedIn is a professional networking platform that connects people with job opportunities, industry experts, and businesses. It allows users to build a professional profile, connect with others in their industry, search for jobs, and showcase their skills and experience. To use LinkedIn effectively, consider the following steps:

Create a professional profile: Start by creating a comprehensive profile that showcases your skills, experience, and education. Use a professional headshot as your profile picture, and write a compelling headline that summarizes what you do and what you offer.

Build a network: Connect with people you know, such as colleagues, classmates, and friends. LinkedIn also allows you to search for and connect with people in your desired industry or field.

Engage with others: Share articles, post updates, and comment on others' posts to increase your visibility and build relationships. This will help you establish yourself as an expert in your field and establish a professional reputation.

Showcase your skills: Highlight your skills and experience by listing them on your profile. You can also ask your connections to endorse or recommend your skills, which will boost your credibility.

Join groups: Join groups that are relevant to your industry or interests. Engage in discussions, share your expertise, and connect with others in the group.

Find job opportunities: Use LinkedIn's job search feature to find job openings that match your skills and experience. You can also use LinkedIn to apply for jobs and reach out to recruiters or hiring managers.

Be consistent: Consistently engage with others on LinkedIn and update your profile with your latest experience, skills, and accomplishments. This will keep your profile active and increase your visibility to potential employers.

By following these steps, you can effectively use LinkedIn to build a professional network, showcase your skills and experience, and find job opportunities.
''')