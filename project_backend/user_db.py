import mysql.connector as sql

# to connect to mysql
conn = sql.connect(host='localhost', user='root', password='Angelina1005!', database='mcq_generator')
cursor = conn.cursor()  # to create a cursor object

class GetUser:
    
    def get_user_password(self,user_email):
        cursor.execute("SELECT user_password FROM user WHERE user_email=%s",(user_email,))
        return cursor.fetchone()

    def get_user_id(self,user_email):
        cursor.execute("SELECT user_id FROM user WHERE user_email=%s",(user_email,))
        return cursor.fetchone()
    
                       
                       
