#  Created by btrif Trif on 28-03-2023 , 1:55 PM.


from dynatrace import Dynatrace
from dynatrace import TOO_MANY_REQUESTS_WAIT
from dynatrace.environment_v2.tokens_api import SCOPE_METRICS_READ, SCOPE_METRICS_INGEST
from dynatrace.configuration_v1.credential_vault import PublicCertificateCredentials

from datetime import datetime, timedelta
import os





# Environment Variables, secrets

token_id = os.environ.get("token_id ")
token_secret = os.environ.get("token_secret ")
environment_id = os.environ.get("environment_id ")


api_token = token_id + "."+ token_secret
dynatrace_env_url = f"https://{environment_id}.live.dynatrace.com/"


# Create a client that handles too many requests (429)
# dt = Dynatrace("environment_url", "api_token", too_many_requests_strategy=TOO_MANY_REQUESTS_WAIT )

# Create a client that automatically retries on errors, up to 5 times, with a 1 second delay between retries
# dt = Dynatrace("environment_url", "api_token", retries=5, retry_delay_ms=1000 )

# Create a client with a custom HTTP timeout of 10 seconds
# dt = Dynatrace("environment_url", "api_token", timeout=10 )





'''
# Get idle CPU for all hosts
for metric in dt.metrics.query("builtin:host.cpu.idle", resolution="Inf"):
    print(metric)

# Print dimensions, timestamp and values for the AWS Billing Metric
for metric in dt.metrics.query("ext:cloud.aws.billing.estimatedChargesByRegionCurrency"):
    for data in metric.data:
        for timestamp, value in zip(data.timestamps, data.values):
            print(data.dimensions, timestamp, value)

# Get all ActiveGates
for ag in dt.activegates.list():
    print(ag)

# Get metric descriptions for all host metrics
for m in dt.metrics.list("builtin:host.*"):
    print(m)

# Delete endpoints that contain the word test
for plugin in dt.plugins.list():

    # This could also be dt.get_endpoints(plugin.id)
    for endpoint in plugin.endpoints:
        if "test" in endpoint.name:
            endpoint.delete(plugin.id)

# Prints dashboard ID, owner and number of tiles
for dashboard in dt.dashboards.list():
    full_dashboard = dashboard.get_full_dashboard()
    print(full_dashboard.id, dashboard.owner, len(full_dashboard.tiles))

# Delete API Tokens that haven't been used for more than 3 months
for token in dt.tokens.list(fields="+lastUsedDate,+scopes"):
    if token.last_used_date and token.last_used_date < datetime.now() - timedelta(days=90):
        print(f"Deleting token! {token}, last used date: {token.last_used_date}")

# Create an API Token that can read and ingest metrics
new_token = dt.tokens.create("metrics_token", scopes=[SCOPE_METRICS_READ, SCOPE_METRICS_INGEST])
print(new_token.token)

# Upload a public PEM certificate to the Credential Vault
with open("ca.pem", "r") as f:
    ca_cert = f.read()

my_cred = PublicCertificateCredentials(
        name="my_cred",
        description="my_cred description",
        scope="EXTENSION",
        owner_access_only=False,
        certificate=ca_cert,
        password="",
        credential_type="PUBLIC_CERTIFICATE",
        certificate_format="PEM"
        )

r = dt.credentials.post(my_cred)
print(r.id)

'''




if __name__ == '__main__':
    '''
        # Create a Dynatrace client
        dt_client = Dynatrace(dynatrace_env_url, api_token)
        # Get all hosts and some properties
        print(f"token_id : {dt_client.tokens.get(token_id)}" )
        # for entity in dt_client.list('type("HOST")', fields="properties.memoryTotal,properties.monitoringMode"):
        #     print(entity.entity_id, entity.display_name, entity.properties)
        mngmt_zone = dt_client.management_zones
        print(f"management_zones :  {mngmt_zone.get(-5914000214989127995)  }")
        dashboards = dt_client.dashboards
    
    
    '''
    import requests
    import json

    zone_url = "https://gss19887.live.dynatrace.com/api/config/v1/managementZones"
    params = {"Api-Token": api_token}
    get_mngmnt_res = requests.get(
            url=zone_url,
                 params=params)
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



