from ..app import cache, toolsdb
import psycopg2.extras
from ..app import logger


# flask-caching can also cache view functions, templates and data explicitly.
# see https://flask-caching.readthedocs.io/en/latest/
@cache.memoize(timeout=30)
def get_items():
    results = []

    cur = toolsdb().cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        SELECT 1 AS id, 'foo' AS name
        UNION
        SELECT 2 AS id, 'bar' AS name;
    """)
    results = cur.fetchall()
    cur.close()

    logger.debug("get_items() db query completed")
    return results
