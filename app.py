from flask import Flask,render_template,request,jsonify,render_template
from models import add_user,get_user_by_email
import pdfplumber
import json
from werkzeug.security import generate_password_hash,check_password_hash
from ai_api import analyze_resume_with_ai

app= Flask(__name__)

@app.route('/')
def home():
    return "Server Running"

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # check file exists in request
        if 'resume' not in request.files:
           return jsonify({"message": "No file uploaded"})

        pdf = request.files['resume']
        JD = request.form['job_description']
        #checks user selected or not
        if pdf.filename == "":
          return jsonify({"message": "please select file"})
        #checks file extension
        if pdf.filename.lower().endswith('.pdf'):
            filename = pdf.filename
            filepath = 'uploads/' + filename
            pdf.save(filepath)
            data = extract_text_from_pdf(filepath)
            feedback = analyze_resume_with_ai(data, JD)
            return render_template("result.html",feedback=feedback)
        return jsonify({"message": "Only PDF files allowed"})    
    else:
        return render_template('upload.html')

def extract_text_from_pdf(filepath):
    raw_text=""
    with pdfplumber.open(filepath) as file:
        for page in file.pages:
            text = page.extract_text()
            if text:
                raw_text+=text

    full_text = raw_text.strip().replace("\n", " ")  # data cleaning
    full_text = " ".join(full_text.split())
    return full_text

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        original_password = request.form.get("password")
        hashed_password = generate_password_hash(original_password)
        user=add_user(name,email,hashed_password)
        return user
    else:
        return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email= request.form.get('email')
        entered_password = request.form.get('password')
        user = get_user_by_email(email)
        if user:
            if check_password_hash(user['password'], entered_password):
                return "Login success"
            return "Invalid password"
        else:
                return "user not found"
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)