import asyncio
from datetime import datetime
import json
from typing import Union

import requests
from settings import DYNATRACE_ENV_URL, API_TOKEN
from utils import load_yaml_file, load_json_file



## find within a dictionary of nested dicts or list keys
def findkeys(node, key_value):
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



def write_value_to_key_in_dict(search_dict: dict, key_name: str, value_name: Union[str, list, dict]):
    ''' write item in a nested dictionary of mixed dicts and lists'''

    for key, value in search_dict.items():

        if key == key_name:
            search_dict[key_name] = value_name
            return search_dict

        elif isinstance(value, dict):
            return write_value_to_key_in_dict(value, key_name, value_name)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    return write_value_to_key_in_dict(item, key_name, value_name)




def get_management_id(id: int):
    ''' GET request to query the management zone id from DynaTrace'''
    GET_ID_URL = ZONE_URL + "/" + str(id)
    params = {"Api-Token": API_TOKEN}
    get_result = requests.get(
            url=GET_ID_URL,
            params=params
            )
    return get_result.json()


def get_management_zones():
    ''' GET request to list all the current management zones from DynaTrace'''
    params = {"Api-Token": API_TOKEN}
    get_result = requests.get(
            url=ZONE_URL,
            params=params
            )
    return get_result.json()


def get_teams_names_from_dict(data: dict, key_name: str) -> list:
    if key_name in data:
        # return [ k for k,v in data[key_name].items() ]
        return data[key_name]
    for k, val in data.items():
        if isinstance(val, dict):
            item = findkeys(val, key_name)
            if next(item) is not None:
                return next(item)


def get_management_zones_names_from_dynatrace() -> list:
    ''' Get all the existing Management Zone Names from DynaTrace'''
    params = {"Api-Token": API_TOKEN}
    try:
        get_result = requests.get(
                url=ZONE_URL,
                params=params
                ).json()['values']
    except Exception:
        print("Cannot get management zones")
    mgmt_names = [val for zones in get_result for mgmt_zone, val in zones.items() if mgmt_zone == 'name']

    return mgmt_names




def compose_data_rules(teams, rules, team_name) ->dict :

    # Get host group prefixes from the teams file
    team_details = find_key_in_nested_dict(teams, team_name )[0]
    print(f"team_details:      {team_details }")
    host_group_prefixes = find_key_in_nested_dict(team_details, "host-group-prefixes")
    print(f"host_group_prefixes = {host_group_prefixes}")

    # Get the rules from the json file




    # print(team_details)
    # new_rules = write_value_to_key_in_dict(json_data, 'value', team_details)
    # print(f"\nnew_rule: {new_rules}")
    # return new_rules

    return teams



def post_management_zone_name_to_dynatrace(zone_name:str, payload_file, yaml_file) -> list:
    ''' Post Management Zone Name from DynaTrace'''
    params = {"Api-Token": API_TOKEN}
    headers = {'content-type': 'application/json'}

    date_time = datetime.now().strftime("%d.%m.%Y") + " " + datetime.now().strftime("%H:%M")

    payload_data = {
        "name" : zone_name,
        "description" : zone_name + ", "+date_time,
        "rules" : [rules],
        }

    print(f"\npayload_data : \n{payload_data}")

    try:
        post_request_result = requests.post(
                url=ZONE_URL,
                params=params,
                data=json.dumps(payload_data),
                headers=headers
                )

        print(f"\npost_request_result: {post_request_result.json()}")

    except Exception:
        print(f"Cannot POST management zone {zone_name}")


    return post_request_result



import sys


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    ZONE_URL = DYNATRACE_ENV_URL + "api/config/v1/managementZones"
    RULES =  load_json_file("rules.json")
    teams_yaml_input_file = str(input("Enter the name of the YML file: "))
    TEAMS = load_yaml_file(teams_yaml_input_file)

    dynatrace_mgmt_zones_result = get_management_zones_names_from_dynatrace()
    print(f"\nDynatrace mgmt_zones : \n{dynatrace_mgmt_zones_result}")


    teams = get_teams_names_from_dict(TEAMS, 'teams')
    print(f"\nteams :\n{teams}")

    # zone_result = get_management_id(104904589338623993)
    # print(f"\nzone_result : \n{zone_result}")

    print("\nPOST / UPDATE")
    for team, val in teams.items():
        if team not in dynatrace_mgmt_zones_result :
            print(f"\nteam_name: {team}   \nval = {val}")
            rules = compose_data_rules(TEAMS, RULES, team)
            # print(f'rules: \n{rules}')



    #         post_management_zone_name_to_dynatrace(team, RULES_FILE, TEAMS_FILE )

