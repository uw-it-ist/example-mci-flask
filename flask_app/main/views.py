from . import main
from . import queries
from flask import render_template, session
from tools.flask.authz import authorize


@main.route("/healthz")
def healthz():
    """
    Test everything that indicates this app is healthy.
    The app may be restarted if this does not return 200.
    Failure of upstream dependencies should be handled gracefully in this app without causing this to fail.
    """
    return 'OK'


@main.route("/")
@authorize()
def index():
    items = queries.get_items()
    return render_template("index.html", items=items)


@main.route("/item/<id>")
@authorize()
def item(id):
    return 'This is item id={} and you are {}'.format(id, session["username"])
