import mysql.connector as sql

# to connect to mysql
conn = sql.connect(host='localhost', user='root', password='Angelina1005!', database='mcq_generator')
cursor = conn.cursor()  # to create a cursor object

class GetSubjectName:
    
    def get_subject_name(self,subject_id):
        cursor.execute("SELECT subject_name FROM subject WHERE subject_id=%s",(subject_id,))
        return cursor.fetchone()
