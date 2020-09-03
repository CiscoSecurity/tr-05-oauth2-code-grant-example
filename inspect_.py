from flask import Blueprint, render_template

from api_handlers import InspectAPIHandler
from utils import required_authorization

inspect_blueprint = Blueprint("inspect", __name__, url_prefix="/inspect")


@inspect_blueprint.route("/", methods=["POST"])
@required_authorization
def inspect():
    info = InspectAPIHandler().inspect_observable()
    return render_template("index.html", observable=info)
