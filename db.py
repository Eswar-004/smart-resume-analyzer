import pymysql
def get_connection():
    return pymysql.connect(
    host = 'localhost',
    user = 'root',
    password = '2889',
    database='project',
    cursorclass=pymysql.cursors.DictCursor
    )
       