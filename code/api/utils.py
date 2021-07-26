import time

from functools import wraps
from flask import session, render_template, abort

from constants import REGION_API_URLS
from api.oauth_handler import OAuth2CTR


def required_authorization(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        oauth_token = session.get("oauth_token")
        if session.get("oauth_token") is None:
            return render_template("index.html",
                                   regions=REGION_API_URLS,
                                   info="You have not login yet :(")
        elif oauth_token["expires_at"] < time.time():
            OAuth2CTR().update_tokens()
            return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return decorated_function
