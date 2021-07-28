from flask import Blueprint, render_template, request

from api.api_handlers import InspectAPI
from api.utils import required_authorization

inspect_blueprint = Blueprint("inspect", __name__, url_prefix="/inspect")


@inspect_blueprint.route("/", methods=["POST"])
@required_authorization
def inspect():
    content = request.form.get("content")
    info = InspectAPI().inspect_observable(content)
    return render_template("index.html", observable=info)
