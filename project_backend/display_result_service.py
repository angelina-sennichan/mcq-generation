from question_db import GetQuestionDataFromDb
from test_db import InsertDataIntoTest
from test_question_map_db import InsertDataIntoTestQuestionMap

question_db_object = GetQuestionDataFromDb()
test_db_object = InsertDataIntoTest()
test_question_map_db_object = InsertDataIntoTestQuestionMap()

class CalculateScore:
    def get_score(self, test_id,answer_list):
        '''
        This function calculates the score for a given test based on the user's answers.       
        param1 test_id: The ID of the test being evaluated.
        param2 answer_list: A list of answers provided by the user.
        returns: A dictionary containing the scored marks and the cut-off marks for the test.
        '''
        question_id_list = test_question_map_db_object.get_question_id_from_test_question_map(test_id)
        for i in range(0,len(question_id_list)):
            test_question_map_db_object.insert_option_selected_by_user(test_id,question_id_list[i][0],answer_list[i])
        correct_answers=[]
        for question_id in question_id_list:
            answer=question_db_object.get_question_answer(question_id[0])
            correct_answers.append(answer[0])
        scored_marks=0
        for i in range(0,len(question_id_list)):
            if(correct_answer[i]==answer_list[i]):
                scored_marks+=1
        cut_off=test_db_object.get_cut_off(test_id)[0]
        test_db_object.insert_scored_mark(scored_marks,test_id)
        return {"marks":scored_marks, "cut_off":cut_off}
