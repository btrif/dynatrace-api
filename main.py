# This is a sample Python script.

# Press <no shortcut> to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
import requests
from settings import DYNATRACE_ENV_URL, API_TOKEN
from utils import load_yaml_file, load_json_file

ZONE_URL = DYNATRACE_ENV_URL + "api/config/v1/managementZones"


def find_key_value_in_dict(data: dict, key_name: str):
    ''' find item in a nested dictionary'''
    if key_name in data:
        return data[key_name]
    for k, val in data.items():
        if isinstance(val, dict):
            item = find_key_value_in_dict(val, key_name)
            if item is not None:
                return item


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
        return [ k for k,v in data[key_name].items() ]
    for k, val in data.items():
        if isinstance(val, dict):
            item = find_key_value_in_dict(val, key_name)
            if item is not None:
                return item


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


def compose_data_payload():
    pass



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mgmt_zones_file = "management_zones.yml"
    payload_file = "payload.json"

    mgmt_zones_result = get_management_zones_names_from_dynatrace()
    print(f"\nmgmt_zones : \n{mgmt_zones_result}")

    yaml_obj = load_yaml_file(mgmt_zones_file)
    print("\n", yaml_obj)

    teams_names = get_teams_names_from_dict(yaml_obj, 'teams')
    print(f'\nteams_names:   {teams_names}')


    # mngmt_data = {
    #     "name": "bogdan-sample-encapsulation",
    #     "description": "bogdan-test 4, 29.03.2023, 12:30 PM",
    #     "rules": [],
    #     "dimensionalRules": [],
    #     "entitySelectorBasedRules": []
    #     }
    #
    # headers = {'content-type': 'application/json'}
