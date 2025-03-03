import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="registration_test"
    )