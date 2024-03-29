from flask import Blueprint, render_template, request

from api.api_handlers import ModuleInstanceAPI
from api.utils import required_authorization

modules_blueprint = Blueprint("modules", __name__, url_prefix="/modules")


@modules_blueprint.route("/")
@required_authorization
def modules():
    modules_api = ModuleInstanceAPI()
    info = modules_api.get_modules()
    return render_template("index.html", modules=info)


@modules_blueprint.route("/", methods=["POST"])
@required_authorization
def post_module():
    modules_api = ModuleInstanceAPI()
    info = modules_api.create_module(request.form.get("name"))
    return render_template("index.html", created_module=info)


@modules_blueprint.route("/delete")
@required_authorization
def delete_module():
    modules_api = ModuleInstanceAPI()
    modules_api.delete_module(request.args.get('module_id'))
    return render_template(
        "index.html",
        info="Successfully deleted module with ID "
             f"{request.args.get('module_id')}",
    )
