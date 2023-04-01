#  Created by btrif Trif on 29-03-2023 , 12:35 PM.

from typing import Generator
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




## find within a dictionary of nested dicts or list keys
def findkeys(node, key_value) -> Generator:
    ''' Generator to retrieve key values in a nested dicts with lists'''
    if isinstance(node, list):
        for elem in node:
            for value in findkeys(elem, key_value):
                yield value

    elif isinstance(node, dict):
        if key_value in node:
            yield node[key_value]
        for element in node.values():
            for value in findkeys(element, key_value):
                yield value


def find_key_in_nested_dict(search_dict, field)-> list:            # Works, but is NAIVE as it returns a list type
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = find_key_in_nested_dict(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = find_key_in_nested_dict(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found


"""     NOT USED
def get_management_id(id: int):
    # GET request to query the management zone id from DynaTrace
    GET_ID_URL = ZONE_URL + "/" + str(id)
    params = {"Api-Token": API_TOKEN}
    get_result = requests.get(
            url=GET_ID_URL,
            params=params
            )
    return get_result.json()


def get_management_zones():
    # GET request to list all the current management zones from DynaTrace
    params = {"Api-Token": API_TOKEN}
    get_result = requests.get(
            url=ZONE_URL,
            params=params
            )
    return get_result.json()

"""


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