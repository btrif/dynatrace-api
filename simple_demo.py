#  Created by btrif Trif on 28-03-2023 , 1:55 PM.

import requests
import json
import asyncio

from datetime import datetime, timedelta
import os

from settings import ENVIRONMENT_ID, API_TOKEN


async def main2():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
    response1 = await future1
    response2 = await future2
    print(response1.text)
    print(response2.text)

# async_req = asyncio.get_event_loop()
# async_req.run_until_complete(main2())



if __name__ == '__main__':
    zone_url = "https://"+ENVIRONMENT_ID+".live.dynatrace.com/api/config/v1/managementZones"
    params = {"Api-Token": API_TOKEN}
    get_mngmnt_res = requests.get(
            url=zone_url,
            params=params
            )
    print('GET request: ')
    print(get_mngmnt_res.json())



    zone_data1 = {
       'name': 'global-pcf-a',
        'description': 'global-pcf-a 31.03.2023 20:02',
        'rules': [
            {'type': 'PROCESS_GROUP', 'enabled': True,
             'propagationTypes': ['PROCESS_GROUP_TO_SERVICE', 'PROCESS_GROUP_TO_HOST'],
             'conditions': [
                {'key': {'attribute': 'HOST_GROUP_NAME'},
                 'comparisonInfo': {'type': 'STRING',
                                    'operator': 'BEGINS_WITH',
                                    'value': ['global-pcf-a-Z', 'global-pcf-a-Y'],
                                    'negate': False,
                                    'caseSensitive': True}
                 }
                 ]
             }
            ],
        "dimensionalRules": [],
        "entitySelectorBasedRules": []
        }


    zone_data2 = {
        "name": "manual_entry_9",
        "description": "01.042023 14:39",
        "rules": [
            {
                "type": "SERVICE",
                "enabled": True,
                "propagationTypes": [
                    "SERVICE_TO_HOST_LIKE"
                    ],
                "conditions": [
                    {
                        "key": {
                            "attribute": "SERVICE_DATABASE_NAME"
                            },
                        "comparisonInfo": {
                            "type": "STRING",
                            "operator": "BEGINS_WITH",
                            "value": "['global-pcf-a-Z', 'global-pcf-a-Y']",
                            "negate": False,
                            "caseSensitive": False
                            }
                        }
                    ]
                }
            ]
        }

    headers = {'content-type': 'application/json'}

    # print('\nPOST request:')
    # post_request_result = requests.post(
    #         url=zone_url,
    #         params=params,
    #         data=json.dumps(zone_data2),
    #         headers=headers
    #         )
    #
    # print(post_request_result.json())

    ID="1781855667665253367"
    zone_update_url = "https://"+ENVIRONMENT_ID+".live.dynatrace.com/api/config/v1/managementZones/"+ID
    print(f"zone_update_url : {zone_update_url}")

    print('\nUPDATE request:')
    try :
        put_request_result = requests.put(
                url=zone_update_url,
                params=params,
                data=json.dumps(zone_data2),
                headers=headers
                )
        print(f"put_request_result: \n {put_request_result}")
    except Exception :
        print('EXCEPTION !')



