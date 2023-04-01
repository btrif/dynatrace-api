from datetime import datetime
import json
import requests
from settings import DYNATRACE_ENV_URL, API_TOKEN
from utils import load_yaml_file, load_json_file, findkeys, find_key_in_nested_dict


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
    except ConnectionError:
        print("Cannot get management zones")

    zones = dict()
    for zone in get_result:
        zones[zone['name']] = zone

    # mgmt_names = [val for zones in get_result for mgmt_zone, val in zones.items() if mgmt_zone == 'name']     ->
    # NOT USED

    return zones


def compose_data_rules_from_team(teams, rules, team_name) -> dict:
    # Get host group prefixes from the teams file
    team_details = find_key_in_nested_dict(teams, team_name)[0]
    host_group_prefixes = find_key_in_nested_dict(team_details, "host-group-prefixes")
    if host_group_prefixes:
        host_group_prefixes = ','.join(host_group_prefixes[0])
        # print(f"host_group_prefixes = {host_group_prefixes}")
    else:
        host_group_prefixes = 'null'

    # Update the rules from the json file
    rules["conditions"][0]["comparisonInfo"]["value"] = host_group_prefixes

    return rules


def post_management_zone_name_to_dynatrace(zone_url: str, zone_name: str, rules: dict) -> list:
    ''' Post Management Zone Name from DynaTrace'''
    params = {"Api-Token": API_TOKEN}
    headers = {'content-type': 'application/json'}
    date_time = datetime.now().strftime("%d.%m.%Y") + " " + datetime.now().strftime("%H:%M")
    payload_data = {
        "name": zone_name,
        "description": zone_name + ", " + date_time,
        "rules": [rules],
        }
    # print(f"\npayload_data : \n{payload_data}")

    try:
        post_request_result = requests.post(
                url=zone_url,
                params=params,
                data=json.dumps(payload_data),
                headers=headers
                )

        if post_request_result.status_code == 204:
            print(f"\npost_request_result: {post_request_result}")
            print(f"{post_request_result.request.body}")
            return post_request_result

    except ConnectionError:
        print(f"Cannot UPDATE management zone {zone_name}")


def update_management_zone_name_to_dynatrace(zone_url: str, zone_id: str, zone_name: str, rules: dict) -> list:
    ''' Post Management Zone Name from DynaTrace'''
    params = {"Api-Token": API_TOKEN}
    headers = {'content-type': 'application/json'}
    date_time = datetime.now().strftime("%d.%m.%Y") + " " + datetime.now().strftime("%H:%M")
    payload_data = {
        "name": zone_name,
        "description": zone_name + ", " + date_time,
        "rules": [rules],
        }
    # print(f"\npayload_data : \n{payload_data}")

    # Get ID of the team_name zone :
    ZONE_ID_URL = zone_url + "/" + zone_id

    try:
        update_request_result = requests.put(
                url=ZONE_ID_URL,
                params=params,
                data=json.dumps(payload_data),
                headers=headers
                )

        if update_request_result.status_code == 204:
            print(f"\nupdate_request_result: {update_request_result}")
            print(f"{update_request_result.request.body}")
            return update_request_result

    except ConnectionError:
        print(f"Cannot UPDATE management zone {zone_name}")


if __name__ == '__main__':

    ZONE_URL = DYNATRACE_ENV_URL + "api/config/v1/managementZones"

    RULES = load_json_file("rules.json")
    teams_yaml_input_file = str(input("Enter the name of the YML file: "))
    TEAMS = load_yaml_file(teams_yaml_input_file)
    # TEAMS = load_yaml_file("teams.yml")

    # Step 0 - Make a list of the existing Management Zones Names
    print("\nGET DynaTrace Management Zones")
    dynatrace_mgmt_zones_result = get_management_zones_names_from_dynatrace()
    print(f"Dynatrace mgmt_zones : \n{dynatrace_mgmt_zones_result}")

    all_teams = get_teams_names_from_dict(TEAMS, 'teams')
    # print(f"\nteams :\n{teams}")

    # zone_result = get_management_id(104904589338623993)
    # print(f"\nzone_result : \n{zone_result}")

    # Take all the teams
    for team_name, val in all_teams.items():
        # STEP2 - POST - If the Management Zone does NOT exist
        if team_name not in dynatrace_mgmt_zones_result:
            print("\nPOST", end=" ")
            print(f"team_name: {team_name}   \nval = {val}")
            updated_rules = compose_data_rules_from_team(TEAMS, RULES, team_name)
            post_management_zone_name_to_dynatrace(ZONE_URL, team_name, updated_rules)
        # STEP 3 - UPDATE - If Management Zone DOES exist
        else:
            print("\nUPDATE", end=" ")
            updated_rules = compose_data_rules_from_team(TEAMS, RULES, team_name)
            zone_id = dynatrace_mgmt_zones_result[team_name]['id']
            print(f'zone_id = {zone_id}')
            update_management_zone_name_to_dynatrace(ZONE_URL, zone_id, team_name, updated_rules)
