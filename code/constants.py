import requests

from flask import abort
from environs import Env

env = Env()
env.read_env()

BASE_URL = "https://visibility.amp.cisco.com"

CLIENT_ID = env.str("CTR_CLIENT_ID")
if not CLIENT_ID:
    abort(500, "Env variable CTR_CLIENT_ID was not specified")

CLIENT_SECRET = env.str("CTR_CLIENT_SECRET")
if not CLIENT_SECRET:
    abort(500, "Env variable CTR_CLIENT_SECRET was not specified")

try:
    REGION_API_URLS = requests.get(
        "https://visibility.amp.cisco.com/clouds.json"
    ).json()
except ValueError:
    abort(500, "Cisco server cannot get available regions")
