#  Created by btrif Trif on 29-03-2023 , 12:35 PM.


import json
import yaml

def yaml_to_json_file(yaml_file, json_file):

    with open(yaml_file, 'r') as yaml_in, open(json_file, "w") as json_out:
        yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
        json.dump(yaml_object, json_out)

    with open(json_file, 'r') as result_file:
            print(result_file.read())


def json_to_yaml_file(json_file, yaml_file):

    with open(json_file, 'r') as json_in, open(yaml_file, "w") as yaml_out:
        json_obj = json.load(json_in)
        yaml_obj = yaml.dump(json_obj, yaml_out)
    print('\nYAML file: ')
    with open(yaml_file, 'r') as result_file:
        print(result_file.read())

def load_json_file(json_file):
    with open(json_file, 'r') as json_in :
        json_obj = json.load(json_in)
    return json_obj

def load_yaml_file(yaml_file):
    with open(yaml_file, 'r') as yaml_in :
        yaml_obj = yaml.safe_load(yaml_in)
    return yaml_obj




def convert_yaml_to_json():
    pass



if __name__ == '__main__':

    teams_yaml_input_file = str(input("Enter the name of the YML file: "))
    TEAMS = load_yaml_file(teams_yaml_input_file)
    json_file = "rules.json"

    # yaml_to_json_file(yaml_file, json_file)
    # json_to_yaml_file(json_file, "management_zones2.yml")
    json1 = load_json_file(json_file)
    print(json1)

    yaml1 = load_yaml_file(teams_yaml_input_file)
    print(yaml1)