import os

from flask import abort

BASE_URL = "https://visibility.amp.cisco.com"

CLIENT_ID = os.getenv("CTR_CLIENT_ID")
CLIENT_SECRET = os.getenv("CTR_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    abort(500, "client_id or client_password wasn't specified")
