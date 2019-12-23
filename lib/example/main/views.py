from . import main
from . import queries as q
from flask import render_template
from tools.flask.session import require_weblogin_authentication


@main.route("/")
@require_weblogin_authentication
def index():
    customers = q.get_customers()
    return render_template("index.html", customers=customers)


@main.route("/whatever/<id>")
@require_weblogin_authentication
def customer(id):
    pass
