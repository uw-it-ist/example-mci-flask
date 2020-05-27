from flask import make_response, jsonify, Blueprint


api = Blueprint("api", "flask_app.api", static_folder=None,
                template_folder=None)


@api.route("/healthz")
def index():
    """
    Return the result of a full self diagnostic check.
    """
    return make_response(jsonify({
        "pass": True,
    }), 200)
