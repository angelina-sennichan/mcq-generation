import mysql.connector as sql

# to connect to mysql
conn = sql.connect(host='localhost', user='root', password='****', database='mcq_generator')
cursor = conn.cursor()  # to create a cursor object

class GetQuestionDataFromDb:
    def get_questions_from_db(self, subject_id):
        cursor.execute("SELECT question FROM question WHERE subject_id=%s",(subject_id,))
        return cursor.fetchall()

    def get_question_with_options_from_db(self, question_id):
        cursor.execute("SELECT question, option_1, option_2, option_3, option_4 FROM question WHERE question_id=%s",(question_id,))
        return cursor.fetchone()

    def get_question_answer(self, question_id):
        cursor.execute("SELECT correct_answer FROM question WHERE question_id=%s",(question_id,))
        return cursor.fetchone()

    def get_question_id(self, question_id):
        cursor.execute("SELECT question_id FROM question WHERE subject_id=%s",(subject_id,))
        return cursor.fetchone()
        
        


