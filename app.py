import os
import time
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import pdfplumber
from dotenv import load_dotenv

from models import add_user, get_user_by_email, add_feedback_history, get_user_feedback_history, get_feedback_by_id
from ai_api import analyze_resume_with_ai

# Load configuration environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "e8f99e3a6c2049d5bf18f0ad562a1c49df5d688cf503e7c8")

# Enforce secure configuration limits
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB file upload limit

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def extract_text_from_pdf(filepath):
    raw_text = ""
    try:
        with pdfplumber.open(filepath) as file:
            for page in file.pages:
                text = page.extract_text()
                if text:
                    raw_text += text
    except Exception as e:
        print(f"Error reading PDF {filepath}: {str(e)}")
        return ""

    full_text = raw_text.strip().replace("\n", " ")  # data cleaning
    full_text = " ".join(full_text.split())
    return full_text

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('upload'))
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Check file exists in request
        if 'resume' not in request.files:
            return render_template('upload.html', error="No file uploaded", user=session.get('user_email'))

        pdf = request.files['resume']
        JD = request.form.get('job_description', '').strip()
        
        if not JD:
            return render_template('upload.html', error="Job description is required.", user=session.get('user_email'))

        # Checks if user selected a file
        if pdf.filename == "":
            return render_template('upload.html', error="Please select a file.", user=session.get('user_email'))

        # Checks file extension
        if not pdf.filename.lower().endswith('.pdf'):
            return render_template('upload.html', error="Only PDF files are allowed.", user=session.get('user_email'))

        # Ensure upload folder exists safely
        os.makedirs('uploads', exist_ok=True)

        # Generate a path traversal-safe, unique filename
        safe_name = secure_filename(pdf.filename)
        unique_filename = f"{session['user_id']}_{int(time.time())}_{safe_name}"
        filepath = os.path.join('uploads', unique_filename)

        try:
            pdf.save(filepath)
            data = extract_text_from_pdf(filepath)
            
            if not data:
                return render_template('upload.html', error="Failed to extract text from PDF. The file may be empty or corrupted.", user=session.get('user_email'))

            # Analyze resume with Groq AI API
            feedback = analyze_resume_with_ai(data, JD)
            
            if isinstance(feedback, str):
                return render_template('upload.html', error=f"AI Analysis Failed: {feedback}", user=session.get('user_email'))

            # Save the record in feedback history under the logged-in user ID
            feedback_id = add_feedback_history(
                user_id=session['user_id'],
                resume_filename=pdf.filename,
                job_description=JD,
                ats_score=feedback.get('ats_score', 0),
                strengths=feedback.get('strengths', []),
                weaknesses=feedback.get('weaknesses', []),
                missing_keywords=feedback.get('missing_keywords', []),
                improvement_plan=feedback.get('improvement_plan', [])
            )
            
            # Post-Redirect-Get pattern to avoid form re-submission on refresh
            return redirect(url_for('result', feedback_id=feedback_id))

        except Exception as e:
            return render_template('upload.html', error=f"Processing error: {str(e)}", user=session.get('user_email'))
        finally:
            # Clean up the file to secure user privacy and save space
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except OSError:
                    pass
    else:
        return render_template('upload.html', user=session.get('user_email'))

@app.route('/result/<int:feedback_id>')
@login_required
def result(feedback_id):
    feedback = get_feedback_by_id(feedback_id)
    if not feedback:
        abort(404, description="Analysis result not found.")

    # Authorization Check: Prevent User A from viewing User B's details
    if feedback['user_id'] != session['user_id']:
        abort(403, description="Access Forbidden. You are not authorized to view this analysis.")

    return render_template("result.html", feedback=feedback)

@app.route('/history')
@login_required
def history():
    history_records = get_user_feedback_history(session['user_id'])
    return render_template("history.html", history=history_records)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('upload'))

    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Server-side validation
        if not name or not email or not password:
            return render_template("register.html", error="All fields are required.")

        # Basic Password Length Validation
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters.")

        # Basic Email Regex Validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return render_template("register.html", error="Invalid email address format.")

        hashed_password = generate_password_hash(password)
        success, msg = add_user(name, email, hashed_password)

        if success:
            return redirect(url_for('login', success_message="Registration successful! Please log in."))
        else:
            return render_template("register.html", error=msg)
    else:
        return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('upload'))

    success_message = request.args.get('success_message')

    if request.method == 'POST':
        email = request.form.get('email', "").strip()
        entered_password = request.form.get('password', "")

        if not email or not entered_password:
            return render_template("login.html", error="Email and Password are required.")

        user = get_user_by_email(email)
        if user:
            if check_password_hash(user['password'], entered_password):
                # Set up session parameters securely
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_name'] = user['name']
                # Maintain compatibility with legacy template links checking session['user']
                session['user'] = user['email']
                return redirect(url_for('upload'))
            return render_template("login.html", error="Invalid password.")
        else:
            return render_template("login.html", error="User email not found.")
    else:
        return render_template("login.html", success_message=success_message)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)