from flask import Blueprint
main = Blueprint("main", "example.main", static_folder="static", template_folder="templates")
api = Blueprint("api", "example.api", static_folder=None, template_folder=None)
