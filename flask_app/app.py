import os
import logging
from flask import Flask, session
from flask_caching import Cache
from whitenoise import WhiteNoise
from tools.flask import db


logging.captureWarnings(True)

cache = Cache(config={
    "CACHE_TYPE": "redis",
    "CACHE_KEY_PREFIX": "example-flask-app",
    "CACHE_REDIS_HOST": os.environ.get("CACHE_REDIS_HOST", 'localhost'),
})


def load():
    app = Flask(__name__, static_folder=None)

    # set flask logging to match gunicorn level
    if __name__ != '__main__':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    app.logger.info("using redis host {}".format(os.environ.get("CACHE_REDIS_HOST", 'localhost')))

    # set a secret key for flask sessions
    app.secret_key = bytes(os.environ["FLASK_SESSION_KEY"], 'utf-8')

    # close database connections explicitly at the end of a request
    app.teardown_appcontext(db.close_connections)

    # cache
    cache.init_app(app)

    # set the env variable APPLICATION_ROOT to the URL path where the app is served
    app.config["APPLICATION_ROOT"] = os.environ.get("APPLICATION_ROOT", "/")
    prefix = app.config["APPLICATION_ROOT"]
    if app.config["APPLICATION_ROOT"] == "/":
        prefix = ""

    # register the blueprint using the prefix defined in the configuration as
    # the application root. if APPLICATION_ROOT is defined incorrectly then
    # this whole thing will break. multiple blueprints may be defined with a
    # different value for "url_prefix" but all blueprints SHOULD begin with the
    # same prefix defined in APPLICATION_ROOT.

    prefix = app.config.get("APPLICATION_ROOT", "")

    # register the blueprint routes at the url_prefix
    from .main import main
    app.logger.info("using application url prefix {}".format(prefix))
    app.register_blueprint(main, url_prefix=prefix)

    from .api import api
    api_prefix = "{}/api".format(prefix)
    app.logger.info("using api url prefix {}".format(api_prefix))
    app.register_blueprint(api, url_prefix=api_prefix)

    # add whitenoise
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

    # make sessions last beyond the browser window instance
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # log the URL paths that are registered
    for url in app.url_map.iter_rules():
        app.logger.debug(repr(url))

    return app
