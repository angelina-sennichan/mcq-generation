import mysql.connector as sql

# to connect to mysql
conn = sql.connect(host='localhost', user='root', password='Angelina1005!', database='mcq_generator')
cursor = conn.cursor()  # to create a cursor object

class InsertDataIntoTestQuestionMap:
    def insert_test_question_map_data(self,test_id,question_id):
        cursor.execute("INSERT INTO test_question_map(test_id,question_id)VALUES(%s,%s)",(test_id,question_id))
        conn.commit()

    def get_question_id_from_test_question_map(self,test_id):
        cursor.execute("SELECT question_id FROM test_question_map WHERE test_id=%s",(test_id,))
        return cursor.fetchall()

    def insert_option_selected_by_user(self,test_id,question_id,option):
        cursor.execute("UPDATE test_question_map SET option_selected=%s WHERE test_id=%s AND question_id=%s",(option,test_id,question_id))      
        conn.commit()
    
        
