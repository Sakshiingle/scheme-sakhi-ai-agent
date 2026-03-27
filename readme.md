
# Scheme Sakhi – AI Agent for Government Schemes

Scheme Sakhi is a voice and text based AI assistant that helps Indian citizens discover relevant central and state government schemes based on their profile (state, category, age, problem).

The goal is to make schemes more accessible for farmers, women, students and senior citizens, especially in Hindi and simple English.

---

## Features

- Multi‑step guided form to collect user details (language, state, category, age, problem).
- AI‑powered scheme recommendations using Google Gemini (with safe fallback when quota is exhausted).
- Hindi and English support with simple, easy‑to‑understand language.
- Voice input for state and problem using Web Speech API.
- Text‑to‑speech for reading out recommended schemes.
- Mobile‑friendly UI with Indian tri‑colour theme.

---

## Tech Stack

- **Backend:** Python, Flask, `google-genai` (Gemini API), `python-dotenv`
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **AI / Agentic:** Gemini model as an agent that takes structured user profile and generates personalised scheme suggestions
- **Other:** Web Speech API (speech‑to‑text and text‑to‑speech)

---

## How to Run Locally

1. Clone the repo:
   git clone https://github.com/Sakshiingle/scheme-sakhi-ai-agent.git
   cd scheme-sakhi-ai-agent
   

2. Create and activate a virtual environment (optional but recommended).

3. Install dependencies:
   py -m pip install -r requirements.txt
   
   or manually: 
   py -m pip install flask google-genai python-dotenv
   

4. Create a `.env` file in the project root:
   GEMINI_API_KEY=YOUR_REAL_GEMINI_API_KEY
  

5. Run the Flask app:
   py app.py
   

6. Open the app in your browser:

   - Go to `http://127.0.0.1:5000`

---

## Notes

- When Gemini free‑tier quota is exhausted, the agent falls back to curated schemes for each category so the user still gets useful recommendations.

