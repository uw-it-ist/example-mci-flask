from . import main
from . import queries
from flask import render_template, request, session
from ..app import logger
import werkzeug.exceptions
import functools


# wrapper for routes that reqire weblogin auth
def require_weblogin_authentication(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        username = request.headers.get("X-Forwarded-User")
        if not username:
            logger.warning("missing X-Forwarded-User header")
            raise werkzeug.exceptions.Unauthorized("You do not have access to this resource. Please try logging in again. (wl)")

        username = username.replace("@washington.edu", "").strip()
        groups = request.headers.get("X-Forwarded-Groups")
        if not groups:
            groups = []
        else:
            groups = groups.split(":")

        session["username"] = username  # xhr and websocket connections can check this for valid sessions
        session["groups"] = groups

        return f(*args, **kwargs)
    return wrapped


@main.route("/healthz")
def healthz():
    """
    Test everything that indicates this app is healthy.
    The app may be restarted if this does not return 200.
    Failure of upstream dependencies should be handled gracefully in this app without causing this to fail.
    """
    return 'OK'


@main.route("/")
@require_weblogin_authentication
def index():
    items = queries.get_items()
    return render_template("index.html", items=items)


@main.route("/item/<id>")
@require_weblogin_authentication
def item(id):
    return 'This is item id=' + id
