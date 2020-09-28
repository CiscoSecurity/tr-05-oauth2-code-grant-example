from flask import Blueprint, render_template, request, session, redirect, abort

from constants import REGION_API_URLS
from oauth_handler import OAuth2CTR
from utils import required_authorization

oauth_blueprint = Blueprint("oauth", __name__)


@oauth_blueprint.route("/")
def homepage():
    return render_template("index.html", regions=REGION_API_URLS)


@oauth_blueprint.route("/login")
def login():
    region = request.args.get("region")
    auth = OAuth2CTR(region=region)

    session["region"] = region

    return redirect(auth.get_authorization_url())


@oauth_blueprint.route("/auth")
def auth():
    if request.args.get("error"):
        return abort(400, request.args.get("error"))

    auth_handler = OAuth2CTR()
    auth_handler.validate_state(request.args.get("state"))
    auth_handler.get_tokens(request.args.get("code"))
    return redirect("/")


@oauth_blueprint.route("/logout")
@required_authorization
def logout():
    session.pop("oauth_token", None)
    return redirect("/")
