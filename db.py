import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prabhat123@i",
        database="student_management"
        //initial commit
    )