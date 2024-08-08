from config import *
from user_config_db import GetUserConfig
from subject_db import GetSubjectName

config_db_object = GetUserConfig()
subject_db_object = GetSubjectName()

def get_test_config_values(user_id):
    """
    Retrieves test configuration values for a given user ID from user configuration files.
    param user_id: The ID of the user for whom the test configurations are to be fetched.
    returns user_test_config_list: A list of dictionaries containing the test configuration values for the user.
    """
    config_files = config_db_object.get_config_by_user_id(user_id)
    user_test_config_list = []
    for file in config_files:
        user_test_config_dict={}
        config_values=config(file[0])
        # Extract subject_id from config_values
        subject_id = config_values["subject_id"]        
        user_test_config_dict["threshold"] = config_values["threshold"]
        user_test_config_dict["subject_id"] = subject_id
        user_test_config_dict["marks"] = config_values["marks"]
        user_test_config_dict["no_of_questions"] = config_values["no_of_questions"]
        user_test_config_dict["cut_off"] = config_values["cut_off"]
        user_test_config_dict["test_duration"] = config_values["test_duration"]
        user_test_config_dict["subject_name"] = subject_db_object.get_subject_name(subject_id)[0]
        user_test_config_list.append(user_test_config_dict)
    return user_test_config_list
        
        
        
        

    
