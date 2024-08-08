import mysql.connector as sql

# to connect to mysql
conn = sql.connect(host='localhost', user='root', password='Angelina1005!', database='mcq_generator')
cursor = conn.cursor()  # to create a cursor object

class InsertDataIntoTest:
    def insert_test_data(self,user_id,subject_id,marks,no_of_questions,cut_off,test_duration):
        cursor.execute("INSERT INTO test(user_id,subject_id,total_mark,total_number_of_questions,cut_off,max_test_duration)VALUES(%s,%s,%s,%s,%s,%s)",(user_id,subject_id,marks,no_of_questions,cut_off,test_duration))
        conn.commit()
        # Retrieve the test_id of the last inserted record
        cursor.execute("SELECT test_id FROM test WHERE user_id = %s ORDER BY test_id DESC LIMIT 1",(user_id,))
        test_tuple = cursor.fetchone()
        test_id = test_tuple[0]
        return test_id

    def get_cut_off(self,test_id):
        cursor.execute("SELECT cut_off FROM test WHERE test_id=%s",(test_id,))
        return cursor.fetchone()

    def insert_scored_mark(self,scored_mark,test_id):
        cursor.execute("UPDATE test SET scored_mark=%s WHERE test_id=%s",(scored_mark,test_id))
        conn.commit()
        
