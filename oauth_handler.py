import time
import uuid
import requests

from urllib.parse import urlencode
from flask import url_for, session, request, abort

from constants import CLIENT_ID, CLIENT_SECRET, BASE_URL


class OAuth2CTR:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.url = f"{BASE_URL}/iroh/oauth2"

    def authorization_url(self):
        """Generates authorization URL to external
        OAuth2 authorization page
        Returns:
            str: Authorization URL
        """
        state = self._generate_state()
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": url_for("oauth.auth", _external=True),
            "scope": "admin integration",
            "state": state,
        }
        session["state"] = state
        auth_url = f"{self.url}/authorize?{urlencode(params)}"

        return auth_url

    def get_tokens(self):
        """Gets access_token, refresh_token etc. by code that OAuth2 external
        service has sent. Saves it in user's session

        Returns:
            dict: token
        """
        url = f"{self.url}/token"

        code = request.args.get("code")
        if not code:
            abort(500, "Authorization code was not provided")

        payload = {
            "grant_type": "authorization_code",
            "redirect_uri": url_for("oauth.auth", _external=True),
            "code": code,
        }

        response = requests.request(
            "POST",
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode(payload),
            auth=self.auth(),
        )
        if response.status_code != 200:
            abort(response.status_code, "Can't get tokens")

        tokens = response.json()
        self._save_token(tokens)

        return tokens

    def update_tokens(self):
        """Updates access_token by refresh token that OAuth2 external
        service has sent. Saves it in user's session

        Returns:
            dict: token
        """
        refresh_token = session.get("oauth_token", {}).get("refresh_token")
        if not refresh_token:
            abort(500, "Refresh token was not provided")

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = requests.request(
            "POST",
            f"{self.url}/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=urlencode(payload),
            auth=self.auth(),
        )
        if response.status_code != 200:
            abort(response.status_code, "Can't get tokens")

        tokens = response.json()
        self._save_token(tokens)

        return tokens

    def auth(self):
        return self.client_id, self.client_secret

    def _save_token(self, token):
        token["expires_at"] = self._get_tokens_expiration_time(token["expires_in"])
        existing_token = session.get("oauth_token")
        if existing_token:
            existing_token.update(token)
        else:
            session["oauth_token"] = token

    @staticmethod
    def _get_tokens_expiration_time(expires_in):
        return time.time() + int(expires_in)

    @staticmethod
    def _generate_state():
        return uuid.uuid4().hex
