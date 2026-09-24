import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

for model in genai.list_models():
    print(model.name)