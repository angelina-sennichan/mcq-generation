import mysql.connector as sql

# to connect to mysql
conn = sql.connect(host='localhost', user='root', password='Angelina1005!', database='mcq_generator')
cursor = conn.cursor()  # to create a cursor object

class GetUserConfig:
    
    def get_config_by_user_id(self,user_id):
        cursor.execute("SELECT config_file FROM user_config_map WHERE user_id=%s",(user_id,))
        return cursor.fetchall()
