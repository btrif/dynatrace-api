#  Created by btrif Trif on 29-03-2023 , 12:35 PM.


import json
import yaml

def convert_yaml_to_json(yaml_file, json_file):

    with open(yaml_file, 'r') as yaml_in, open(json_file, "w") as json_out:
        yaml_object = yaml.safe_load(yaml_in) # yaml_object will be a list or a dict
        json.dump(yaml_object, json_out)

    with open(json_file, 'r') as result_file:
            print(result_file.read())


def convert_json_to_yaml(json_file, yaml_file):

    with open(json_file, 'r') as json_in, open(yaml_file, "w") as yaml_out:
        json_obj = json.load(json_in)
        yaml_obj = yaml.dump(json_obj, yaml_out)
    print('\nYAML file: ')
    with open(yaml_file, 'r') as result_file:
        print(result_file.read())






if __name__ == '__main__':

    yaml_file = "management_zones.yml"
    json_file = "management_zones.json"

    convert_yaml_to_json(yaml_file, json_file)

    convert_json_to_yaml(json_file, "management_zones2.yml")