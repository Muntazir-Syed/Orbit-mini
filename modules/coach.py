import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


def ask_orbit(prompt):
    try:
        if not prompt.strip():
            return "Please enter a question."

        if not API_KEY:
            return (
                "AI Coach is not configured.\n\n"
                "Create a .env file and add:\n"
                "GEMINI_API_KEY=your_api_key"
            )

        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text

        return "No response received."

    except Exception as e:
        return f"Error: {str(e)}"
