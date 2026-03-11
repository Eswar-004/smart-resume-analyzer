# Smart Resume Analyzer

AI-powered web application that analyzes resumes and provides feedback to improve them.

## Features
- Upload resume (PDF)
- Extract resume text using pdfplumber
- AI-powered resume feedback using Groq API
- User authentication (login and register)
- Resume analysis result page
- History tracking

## Tech Stack
- Python
- Flask
- MySQL
- HTML 
- Groq API

## Project Structure

smart-resume-analyzer
│
├── app.py
├── ai_api.py
├── db.py
├── models.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── upload.html
│   ├── result.html
│   └── history.html
├── static/
└── .gitignore


## How to Run

1. Clone the repository

git clone https://github.com/Eswar-004/smart-resume-analyzer.git

2. Install dependencies

pip install -r requirements.txt

3. Run the application

python app.py


## Author

Eswara Perumal
