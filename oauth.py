from flask import Blueprint, render_template, request, session, abort, redirect

from oauth_handler import OAuth2CTR
from utils import required_authorization

oauth_blueprint = Blueprint("oauth", __name__)


@oauth_blueprint.route("/")
def homepage():
    user = session.get("user")
    return render_template("index.html", user=user)


@oauth_blueprint.route("/login")
def login():
    auth = OAuth2CTR()
    return redirect(auth.authorization_url())


@oauth_blueprint.route("/auth")
def auth():
    state = request.args.get("state")
    session_state = session.get("state")
    if state != session_state:
        abort(400, "State has been corrupted")
    OAuth2CTR().get_tokens()
    return redirect("/")


@oauth_blueprint.route("/logout")
@required_authorization
def logout():
    session.pop("oauth_token", None)
    return redirect("/")
