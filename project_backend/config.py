import json

def config(file_name):
    with open(file_name,'r') as file:
        config_values = json.load(file)
    return config_values

'''
import json

def load_config(file_path):
    with open(file_path, 'r') as json_file:
        config = json.load(json_file)
    return config

# Example usage
config_path = 'config.json'
config_data = load_config(config_path)

# Return the loaded configuration
print(config_data)
print("---")
# If you want to access and return individual values:
threshold = config_data.get('threshold')
subject_id = config_data.get('subject_id')
cut_off = config_data.get('cut_off')
modules = config_data.get('modules')

# Return individual values
print("Threshold:", threshold)
print("Subject ID:", subject_id)
print("Cut Off:", cut_off)
print("Modules:", modules)
'''
