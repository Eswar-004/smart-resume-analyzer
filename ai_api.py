import os
from groq import Groq
import json

def analyze_resume_with_ai(data, JD):
    data = data[:4000]
    JD = JD[:4000]

    prompt = f"""
You are an ATS resume screening system.

Compare the resume with the job description.

Return ONLY pure JSON.
Do NOT add explanation.
Do NOT add markdown.
Do NOT add text before or after JSON.
Give 70+ only for top resume rest others give 30 to 50 and if it is not a resume give less than 10.

IMPORTANT:
- Be strict
- Don't over-score
- No random scoring

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
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return {"error": "GROQ_API_KEY not set"}

        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            response_format={"type": "json_object"}  # Forces valid JSON
        )

        return json.loads(completion.choices[0].message.content)

    except json.JSONDecodeError:
        return {"error": "Model returned invalid JSON"}

    except Exception as e:
        return {"error": str(e)}