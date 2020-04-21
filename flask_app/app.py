import os
import logging
from flask import Flask, session
from flask_caching import Cache
import tools.constants
import tools.flask.session
from tools.flask.extensions.database import DatabaseClient
from tools.flask.extensions import cache_buster

# enable a logger
logging.captureWarnings(True)
logger = logging.getLogger(__name__)

# things defined here get used by views and need to be exported by __init__.py
db_client = DatabaseClient()
tools_db_client = DatabaseClient()
storage_db_client = DatabaseClient()
cache = Cache(config={
    "CACHE_TYPE": "memcached",
    "CACHE_KEY_PREFIX": "example-web",
    "CACHE_MEMCACHED_SERVERS": tools.constants.MEMCACHED_CLUSTER_ADDRESS,
})


def load():
    app = Flask(__name__, static_folder=None)
    if ("FLASK_CONFIG" in os.environ):
        app.config.from_envvar("FLASK_CONFIG")

    # set a secret key for sessions
    app.secret_key = tools.flask.session.get_secret_key()

    # cache
    cache.init_app(app)

    # initialize postgres database connection pool
    # remove the databases that you are not using
    db_client.init_app(app, "ripit", **(tools.constants.RIPIT_DSNS.get(app.config.get("ENVIRONMENT"))))
    tools_db_client.init_app(app, "toolsdb", **(tools.constants.TOOLSDB_DSNS.get(app.config.get("ENVIRONMENT"))))
    storage_db_client.init_app(app, "ironfist", **(tools.constants.IRONFISTDB_DSNS.get(app.config.get("ENVIRONMENT"))))
    db_client.init_app(app, "tscdb", **(tools.constants.TSCDB_DSNS.get(app.config.get("ENVIRONMENT"))))

    # initialize the cache busting
    cache_buster.init_app(app)

    # register the blueprint using the prefix defined in the configuration as
    # the application root. if APPLICATION_ROOT is defined incorrectly then
    # this whole thing will break. multiple blueprints may be defined with a
    # different value for "url_prefix" but all blueprints SHOULD begin with the
    # same prefix defined in APPLICATION_ROOT.
    from .main import main
    prefix = app.config.get("APPLICATION_ROOT", "")
    logger.info("using application url prefix {}".format(prefix))
    app.register_blueprint(main, url_prefix=prefix)

    # this is the health api
    from .api import api
    api_prefix = "{}/api".format(prefix)
    logger.info("using api url prefix {}".format(api_prefix))
    app.register_blueprint(api, url_prefix=api_prefix)

    # make sessions last beyond the arbitrary browser session
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # tell ourselves what we've mapped.
    if (logger.isEnabledFor(logging.DEBUG)):
        for url in app.url_map.iter_rules():
            logger.debug(repr(url))

    return app
