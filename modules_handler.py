import requests
from flask import session, request, abort

from constants import BASE_URL


class ModulesAPI:
    def __init__(self):
        self.url = f"{BASE_URL}/iroh/iroh-int/module-instance"
        self.headers = {
            "Accept": "application/json",
            "Authorization": f'Bearer {session["oauth_token"]["access_token"]}',
            "Content-Type": "application/json",
        }

    def get_modules(self):
        response = requests.request("GET", self.url, headers=self.headers)
        if response.status_code != 200:
            abort(response.status_code, "Can't get modules")
        return response.json()

    def create_module(self):
        payload = {
            "name": request.form.get("name"),
            "module_type_id": "a89161ba-8d70-4ea9-a190-1453a763d84f",
            "settings": {
                "url": "https://kt093m2r7d.execute-api.us-east-1.amazonaws.com/dev"
            },
            "enabled": True,
            "visibility": "org",
        }

        response = requests.request(
            "POST", self.url, headers=self.headers, json=payload
        )
        if response.status_code != 201:
            abort(response.status_code, "Can't create modules")

        return response.json()

    def delete_module(self):
        delete_url = f"{self.url}/{request.args.get('module_id')}"
        response = requests.request("DELETE", delete_url, headers=self.headers)
        if response.status_code != 204:
            abort(response.status_code, "Can't delete modules")
        return response.status_code
