from gtts import gTTS
from IPython.display import Audio
import streamlit as st

def tts(text):
    tts = gTTS(text)
    tts.save("tts.mp3")
    return Audio("tts.mp3", autoplay=True)


