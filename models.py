import json
import pymysql
from db import get_connection

def add_user(name, email, password):       # Register
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            connection.commit()
            return True, "User registered successfully"
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                return False, "Email address is already registered."
            return False, f"Integrity error: {str(e)}"
        except Exception as e:
            return False, f"Database error: {str(e)}"
        finally:
            connection.close()

def get_user_by_email(email):          # Login
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user
        finally:
            connection.close()

def add_feedback_history(user_id, resume_filename, job_description, ats_score, strengths, weaknesses, missing_keywords, improvement_plan):
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query = """
                INSERT INTO feedback_history 
                (user_id, resume_filename, job_description, ats_score, strengths, weaknesses, missing_keywords, improvement_plan)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                user_id, 
                resume_filename, 
                job_description, 
                ats_score, 
                json.dumps(strengths), 
                json.dumps(weaknesses), 
                json.dumps(missing_keywords), 
                json.dumps(improvement_plan)
            ))
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()

def get_user_feedback_history(user_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query = """
                SELECT id, user_id, resume_filename, job_description, ats_score, created_at 
                FROM feedback_history 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
        finally:
            connection.close()

def get_feedback_by_id(feedback_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query = "SELECT * FROM feedback_history WHERE id = %s"
            cursor.execute(query, (feedback_id,))
            record = cursor.fetchone()
            if record:
                # Parse JSON fields safely back to Python objects
                for field in ['strengths', 'weaknesses', 'missing_keywords', 'improvement_plan']:
                    if record[field] is not None:
                        if isinstance(record[field], str):
                            try:
                                record[field] = json.loads(record[field])
                            except json.JSONDecodeError:
                                pass
            return record
        finally:
            connection.close()