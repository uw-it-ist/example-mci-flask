from flask import Blueprint
main = Blueprint("main", "flask_app.main", static_folder="static", template_folder="templates")
api = Blueprint("api", "flask_app.api", static_folder=None, template_folder=None)
