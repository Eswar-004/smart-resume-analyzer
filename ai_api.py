import os
from groq import Groq
import json

connection = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume_with_ai(data,JD):
    data = data[:4000]
    JD = JD[:4000]
    prompt = f"""
You are an ATS resume screening system.

Compare the resume with the job description.

Return ONLY pure JSON.
Do NOT add explanation.
Do NOT add markdown.
Do NOT add text before or after JSON.
Give 70+ only for top resume rest others give 40 to 60.

Follow this Strict format:

{{
"ats_score": integer,
"strengths": [
"Mention section name like 'Skills: ...'",
"Mention section name like 'Experience: ...'"
],
"weaknesses": [
"Mention section name like 'Projects: ...'",
"Mention section name like 'Formatting: ...'"
],
"missing_keywords": [],
"improvement_plan": []
}}

RESUME:
{data}

JOB DESCRIPTION:
{JD}
"""
    try:
        completion = connection.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        ai_text = completion.choices[0].message.content
        print("ai:",ai_text)
        ai_json = json.loads(ai_text)
        return ai_json
      
    except Exception as e:
        return str(e)