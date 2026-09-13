import mysql.connector

conn=mysql.connector.connect(host="localhost", username="root", password="123keshav", database="face_recognizer1")
cursor = conn.cursor()
cursor.execute("show databases")

data = cursor.fetchall()

print(data)

conn.close()