from flask import Flask, jsonify, request
from flask_cors import CORS
from user_db import GetUser
from config_display_service import *
from generate_mcq_service import GenerateMCQService
from display_result_service import CalculateScore
import re

app = Flask(__name__)
CORS(app)

class ThresholdIsEmptyError(Exception):
    pass

class ThresholdNotNumberError(Exception):
    pass

class SubjectIdIsEmptyError(Exception):
    pass

class SubjectIdNotIntegerError(Exception):
    pass

class MarksIsEmptyError(Exception):
    pass

class MarksNotIntegerError(Exception):
    pass

class NoOfQuestionsIsEmptyError(Exception):
    pass

class NoOfQuestionsNotIntegerError(Exception):
    pass

class CutOffIsEmptyError(Exception):
    pass

class CutOffNotIntegerError(Exception):
    pass

class TestDurationIsEmptyError(Exception):
    pass

class TestDurationNotTimeFormatError(Exception):
    pass

class AnswerListEmptyError(Exception):
    pass

# API endpoint to authenticate user and fetch test configurations
@app.route('/user', methods=['POST'])
def user_authenticate():
    '''
    Authenticate the user and fetch test configurations.    
    returns: JSON response with a message,test configurations,and user ID.
    '''
    data = request.get_json()
    user_email = data.get('user_email')
    user_password = data.get('user_password')
    user_db_object = GetUser()
    user_id = user_db_object.get_user_id(user_email)
    password = user_db_object.get_user_password(user_email)
    if user_password != password[0]:
        response = {'message': 'Incorrect password. Please enter correct password.'}
        return jsonify(response)
    test_configs = get_test_config_values(user_id[0])
    response = {'message': 'Successful', 'test_configs': test_configs, 'user_id': user_id}
    return jsonify(response)

# API endpoint to show test mcq questions generated
@app.route('/test', methods=['POST'])
def mcq_test_display():
    '''
    Generate and display MCQ test questions.    
    raises ThresholdIsEmptyError: If the threshold value is empty.
    raises ThresholdNotNumberError: If the threshold value is not a number.
    raises SubjectIdIsEmptyError: If the subject ID is empty.
    raises SubjectIdNotIntegerError: If the subject ID is not an integer.
    raises MarksIsEmptyError: If the marks value is empty.
    raises MarksNotIntegerError: If the marks value is not an integer.
    raises NoOfQuestionsIsEmptyError: If the number of questions is empty.
    raises NoOfQuestionsNotIntegerError: If the number of questions is not an integer.
    raises CutOffIsEmptyError: If the cut-off value is empty.
    raises CutOffNotIntegerError: If the cut-off value is not an integer.
    raises TestDurationIsEmptyError: If the test duration is empty.
    raises TestDurationNotTimeFormatError: If the test duration is not in the correct time format.   
    returns: JSON response with MCQ questions and test ID, or error messages.
    '''
    data = request.get_json()
    try:
        threshold = data.get('threshold')
        if threshold is None:
            raise ThresholdIsEmptyError
        if not isinstance(threshold, (int, float)):
            raise ThresholdNotNumberError
    except ThresholdIsEmptyError:
        return jsonify({'message': 'Threshold value is empty. Please provide a number.'}), 400
    except ThresholdNotNumberError:
        return jsonify({'message': 'Entered threshold value is not of valid input. Please provide a number.'}), 400
    try:
        subject_id = data.get('subject_id')
        if subject_id is None:
            raise SubjectIdIsEmptyError
        if not isinstance(subject_id, int):
            raise SubjectIdNotIntegerError
    except SubjectIdIsEmptyError:
        return jsonify({'message': 'Subject ID is empty. Please provide a valid Subject ID.'}), 400
    except SubjectIdNotIntegerError:
        return jsonify({'message': 'Entered Subject ID value is not of valid input. Please provide a number.'}), 400
    try:
        marks = data.get('marks')
        if marks is None:
            raise MarksIsEmptyError
        if not isinstance(marks, int):
            raise MarksNotIntegerError
    except MarksIsEmptyError:
        return jsonify({'message': 'Marks value is empty. Please provide a valid Marks value.'}), 400
    except MarksNotIntegerError:
        return jsonify({'message': 'Entered Marks value is not of valid input. Please provide a number.'}), 400
    try:
        no_of_questions = data.get('no_of_questions')
        if no_of_questions is None:
            raise NoOfQuestionsIsEmptyError
        if not isinstance(no_of_questions, int):
            raise NoOfQuestionsNotIntegerError
    except NoOfQuestionsIsEmptyError:
        return jsonify({'message': 'Number of questions is empty. Please provide a valid number of questions.'}), 400
    except NoOfQuestionsNotIntegerError:
        return jsonify({'message': 'Entered Number of Questions value is not of valid input. Please provide a number.'}), 400
    try:
        cut_off = data.get('cut_off')
        if cut_off is None:
            raise CutOffIsEmptyError
        if not isinstance(cut_off, int):
            raise CutOffNotIntegerError
    except CutOffIsEmptyError:
        return jsonify({'message': 'Cut-off value is empty. Please provide a valid Cut-off value.'}), 400
    except CutOffNotIntegerError:
        return jsonify({'message': 'Entered Cut-off value is not of valid input. Please provide a number.'}), 400
    try:
        test_duration = data.get('test_duration')
        if test_duration is None:
            raise TestDurationIsEmptyError
        if not re.match(r'^\d{1,2}:\d{2}:\d{2}$', test_duration):
            raise TestDurationNotTimeFormatError
    except TestDurationIsEmptyError:
        return jsonify({'message': 'Test duration is empty. Please provide a valid test duration.'}), 400
    except TestDurationNotTimeFormatError:
        return jsonify({'message': 'Entered Test Duration value is not of valid input. Please provide a time in the format hours:minutes:seconds.'}), 400

    user_id = data.get('user_id')
    generator = GenerateMCQService(user_id, threshold, subject_id, marks, no_of_questions, cut_off, test_duration)
    mcq_list, test_id = generator.question_similarity_checker(no_of_questions)
    response = {'mcq_questions': mcq_list, 'test_id': test_id}
    return jsonify(response)

# API endpoint to show test result
@app.route('/result', methods=['POST'])
def result_display():
    '''
    Display the test result based on the user's answers.    
    raises AnswerListEmptyError: If the answer list is empty.    
    returns: JSON response with the test result.
    '''
    data = request.get_json()
    try:
        test_id = data.get('test_id')
        answer_list = data.get('answer_list')
        if not answer_list:
            raise AnswerListEmptyError
    except AnswerListEmptyError:
        return jsonify({'message': 'Answer list is empty. Please provide a valid answer list.'}), 400
    result_object = CalculateScore()
    response = result_object.get_score(test_id, answer_list)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
