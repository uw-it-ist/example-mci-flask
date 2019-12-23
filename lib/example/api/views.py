from . import api
from flask import make_response, jsonify


@api.route("/health/check")
def index():
    return make_response(jsonify({
        "pass": True,
    }), 200)
