import requests
from flask import session, abort

from api.constants import BASE_URL


class BaseAPI:
    url: str

    def _get(self, *args, **kwargs):
        return self.__request("GET", *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self.__request("POST", *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self.__request("PUT", *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self.__request("DELETE", *args, **kwargs)

    def __request(self, method, *args, **kwargs):
        response = requests.request(method, *args, **kwargs)
        if not response.ok:
            abort(response.status_code,
                  f"Failed to {method} data ({self.url})")
        try:
            return response.json()
        except ValueError:
            return {}


class ModuleInstanceAPI(BaseAPI):
    url = f"{BASE_URL}/iroh/iroh-int/module-instance"

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f'Bearer '
                             f'{session["oauth_token"]["access_token"]}',
            "Content-Type": "application/json",
        }

    def get_modules(self):
        return self._get(self.url, headers=self.headers)

    def create_module(self, name):
        payload = {
            "name": name,
            "module_type_id": "a89161ba-8d70-4ea9-a190-1453a763d84f",
            "settings": {
                "url": "https://example.com/relay"
            },
            "enabled": True,
            "visibility": "org",
        }

        return self._post(self.url, headers=self.headers, json=payload)

    def delete_module(self, module_id):
        delete_url = f"{self.url}/{module_id}"
        return self._delete(delete_url, headers=self.headers)


class InspectAPI(BaseAPI):
    url = f"{BASE_URL}/iroh/iroh-inspect/inspect"

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "Authorization": f'Bearer '
                             f'{session["oauth_token"]["access_token"]}',
            "Content-Type": "application/json",
        }

    def inspect_observable(self, content):
        payload = {
            "content": content
        }

        return self._post(self.url, headers=self.headers, json=payload)
