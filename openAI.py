
import os
import openai
class CallAI:
    def getAI(self, text):   
        api_key = os.environ.get("OPENAI_API_KEY")

        # Use the API key
        openai.api_key = api_key

        # Import the OpenAI library


        # Use the API key
<<<<<<< HEAD
        openai.api_key = st.secrets["OPENAI_API_KEY"]
=======
        openai.api_key = "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"
>>>>>>> 90e185e5a7414d7937cfb85e919ad40ad08cc76c

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

        prompt = (f"rewrite the following text:\n{text}")
        return (generate_text(prompt))
