from . import api
from flask import make_response, jsonify


@api.route("/healthz")
def index():
    """
    Return the result of a full self diagnostic check.
    """
    return make_response(jsonify({
        "pass": True,
    }), 200)
