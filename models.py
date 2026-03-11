from db import get_connection
def add_user(name,email,password):       #Register
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query = "insert into users(name,email,password) values(%s,%s,%s)"
            cursor.execute(query,(name,email,password))
            connection.commit()
            return "User added"
        finally:
            connection.close()
def get_user_by_email(email):          #Login
    connection = get_connection()
    with connection.cursor() as cursor:
        try:
            query="select * from users where email = %s"
            cursor.execute(query,(email,))
            user = cursor.fetchone()
            return user
        finally:
            connection.close()
        