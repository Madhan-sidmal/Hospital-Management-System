import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',         # Change to your MySQL username
        password='madhan@g15',  # Change to your MySQL password
        database='hospital_management1'
    )
    return connection
