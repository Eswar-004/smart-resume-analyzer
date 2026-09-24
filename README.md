# Smart Resume Analyzer

AI-powered web application that analyzes resumes and provides personalized feedback to help users improve their resumes.

## Live Demo

**Hosted on AWS EC2**

**Live Application:** `http://13.126.224.72`

## Features

* PDF Resume Upload
* Resume Text Extraction using pdfplumber
* AI-Powered Resume Analysis using Groq API
* ATS Compatibility Score Generation
* Strengths Identification
* Weakness Analysis
* Missing Keywords Detection
* Personalized Improvement Suggestions
* User Registration & Login
* Analysis History Tracking

## Tech Stack

### Backend

* Python
* Flask
* MySQL
* Gunicorn

### Frontend

* HTML
* CSS
* JavaScript

### AI

* Groq API

### Deployment & Infrastructure

* AWS EC2
* Nginx
* Gunicorn
* Systemd
* GitHub

## Project Structure

```text
smart-resume-analyzer/
│
├── app.py
├── ai_api.py
├── db.py
├── models.py
├── templates/
├── static/
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/Eswar-004/smart-resume-analyzer.git
cd smart-resume-analyzer
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

## AWS Deployment

The application is deployed on an **AWS EC2 instance**.

### Production Architecture

```text
User
  ↓
Nginx
  ↓
Gunicorn
  ↓
Flask Application
  ↓
MySQL Database
  ↓
Groq API
```

### Deployment Components

* **AWS EC2** – Hosts the Flask application
* **Nginx** – Reverse proxy and public entry point
* **Gunicorn** – Production WSGI server
* **Systemd** – Application process management
* **MySQL** – Stores application data and analysis history
* **Groq API** – AI-powered resume analysis
* **GitHub** – Source code management

## Deployment Workflow

```text
Local Development
       ↓
     Git
       ↓
    GitHub
       ↓
   AWS EC2
       ↓
    Gunicorn
       ↓
     Nginx
       ↓
   Production
```

## Author

**Eswara Perumal S**

GitHub: https://github.com/Eswar-004

## License

This project is licensed under the MIT License.
