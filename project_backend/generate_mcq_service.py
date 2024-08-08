import random
from question_db import GetQuestionDataFromDb
from test_db import InsertDataIntoTest
from test_question_map_db import InsertDataIntoTestQuestionMap
from similarity_checker import SimilarityChecker

question_db_object = GetQuestionDataFromDb()
test_db_object = InsertDataIntoTest()
test_question_map_db_object = InsertDataIntoTestQuestionMap()

class QuestionIsEmptyError(Exception):
    pass

class QuestionIsDigitError(Exception):
    pass

class GenerateMCQService:
    def __init__(self, user_id, threshold, subject_id, marks, no_of_questions, cut_off, test_duration):
        '''
        This is the constructor function.        
        param1 user_id: The ID of the applicant taking the test.
        param2 threshold: The threshold value for similarity comparison.
        param3 subject_id: The ID of the subject for which the test is being created.
        param4 marks: The total marks for the test.
        param5 no_of_questions: The number of questions in the test.
        param6 cut_off: The cut-off marks for the test.
        param7 test_duration: The duration of the test
        '''
        self.user_id = user_id
        self.threshold = threshold
        self.subject_id = subject_id
        self.marks = marks
        self.no_of_questions = no_of_questions
        self.cut_off = cut_off
        self.test_duration = test_duration

    def question_similarity_checker(self, no_of_questions):
        '''
        This function generates a list of multiple-choice questions while ensuring no significant similarity between them.       
        param1 no_of_questions: The number of questions to be included in the test.        
        returns final_q_list,test_id: A tuple containing the final list of selected questions and the test ID.
        raises QuestionIsEmptyError: Raises exception if question taken is empty.
        raises QuestionIsDigitError: Raises exception if question taken contains just digits.
        '''
        question_bank_list = question_db_object.get_questions_from_db(self.subject_id)
        print("The question bank list is:",question_bank_list)
        similarity_checker_object = SimilarityChecker(self.threshold)
        mcq_list = []
    
        # Avoid infinite loop if question_bank_list is empty
        if not question_bank_list:
            return {"No questions available in the database"}, 500

        while len(mcq_list) < no_of_questions:
            q_taken = random.choice(question_bank_list)
            q_text = q_taken[0]  # Unpack the tuple to get the question text
                
            try:
                if not q_text.strip():  # Check for empty or whitespace-only questions
                    raise QuestionIsEmptyError("The question taken is empty.")
                if q_text.isdigit():  # Check if the question contains only digits
                    raise QuestionIsDigitError("The question taken contains just digits.")
            except QuestionIsEmptyError as e:
                print(f"{e}")
                break
            except QuestionIsDigitError as e:
                print(f"{e}")
                break

            # Check if the question is sufficiently different from existing MCQs
            if similarity_checker_object.is_similar(mcq_list, q_text):
                mcq_list.append(q_text)  # Append the question only if it is sufficiently different

        final_q_list = []
        for question_text in mcq_list:
            question = question_db_object.get_question_with_options_from_db(question_text)
            question_dict = {
                "question": question[0],
                "option_1": question[1],
                "option_2": question[2],
                "option_3": question[3],
                "option_4": question[4]
            }
            final_q_list.append(question_dict)

        test_id = test_db_object.insert_test_data(self.user_id, self.subject_id, self.marks, self.no_of_questions, self.cut_off, self.test_duration)

        question_ids = []
        for question_text in mcq_list:
            question_id = question_db_object.get_question_id(question_text)
            question_ids.append(question_id)

        for q_id in question_ids:
            test_question_map_db_object.insert_test_question_map_data(test_id, q_id)

        return final_q_list, test_id


        
               

       
    
 
        
    
    
