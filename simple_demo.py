#  Created by btrif Trif on 28-03-2023 , 1:55 PM.

import requests
import json

from datetime import datetime, timedelta
import os

# Environment Variables, secrets
token_id = os.environ.get("token_id")
token_secret = os.environ.get("token_secret")
environment_id = os.environ.get("environment_id")
print(f"environment_id : {environment_id}")


api_token = token_id + "." + token_secret
dynatrace_env_url = f"https://{environment_id}.live.dynatrace.com/"


if __name__ == '__main__':
    zone_url = "https://"+environment_id+".live.dynatrace.com/api/config/v1/managementZones"
    params = {"Api-Token": api_token}
    get_mngmnt_res = requests.get(
            url=zone_url,
            params=params
            )
    print('GET request: ')
    print(get_mngmnt_res.json())

    print('request POST')

    mngmt_data = {
        "name": "bogdan-sample-encapsulation",
        "description": "bogdan-test 4, 29.03.2023, 12:30 PM",
        "rules": [],
        "dimensionalRules": [],
        "entitySelectorBasedRules": []
        }

    headers = {'content-type': 'application/json'}

    print('\nPOST request:')
    post_request_result = requests.post(
            url=zone_url,
            params=params,
            data=json.dumps(mngmt_data),
            headers=headers
            )

    print(post_request_result.json())
