import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv() #to load env file

api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "No API key found. Set GROQ_API_KEY or OPENAI_API_KEY in the environment or .env file."
    )

client = Groq(api_key=api_key)

def medical_response(user_input: str):

    system_prompt = """
    You are strictly a medical assistant.
    You must ONLY answer health-related questions.
    If the user asks anything unrelated to health,
    respond with:
    'I am a medical chatbot. Please ask health-related questions only.'
    Never answer non-medical questions.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.5 #creativity of AI responses(balanced)
    )

    return response.choices[0].message.content