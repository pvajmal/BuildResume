
import os
import openai
import streamlit as st
class CallAI:
    def getAI(self, text):   
        # Use the API key
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        #openai.api_key = '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'

        def generate_text(prompt):
            completions = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )

            message = completions.choices[0].text
            return message.strip()

        
        return (generate_text(text))
