#  Created by btrif Trif on 30-03-2023 , 11:59 AM.

from utils import load_json_file


SECRETS = load_json_file(".secrets.json")

# Environment Variables, secrets
TOKEN_ID = SECRETS["token_id"]
TOKEN_SECRET = SECRETS["token_secret"]
ENVIRONMENT_ID = SECRETS["environment_id"]

API_TOKEN = TOKEN_ID + "." + TOKEN_SECRET
DYNATRACE_ENV_URL = f"https://{ENVIRONMENT_ID}.live.dynatrace.com/"

