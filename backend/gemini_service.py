import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
from models import ResourceExhaustedI

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")

def evaluate_candidate(data: dict):
    prompt = f"""
        You are a strict technical hiring evaluator.

        Evaluate the candidate for:
        - Backend Developer
        - Frontend Developer
        - Data Analyst
        - DevOps Engineer

        Scoring Rules:
        80-100 = Strong alignment
        60-79 = Moderate
        40-59 = Weak
        Below 40 = Not suitable

        Return ONLY valid JSON in this format:
        {{
        "roles": [
            {{
            "role": "",
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "improvement_steps": []
            }}
        ],
        "best_fit": "",
        "summary": ""
        }}

        Candidate Data:
        Resume:
        {data["resume_text"]}

        GitHub:
        {data["github_link"]}

        LinkedIn:
        {data["linkedin_link"]}
        """

    try:
        response = model.generate_content(prompt)
    except ResourceExhaustedI:
        return {
        "error": "Daily AI quota exceeded. Please try again later."
        }

    text = response.text.strip()

    if text.startswith("```"):
        text = re.sub(r"```json|```", "", text).strip()

    return json.loads(text)