from ..app import db_client
from ..app import cache


# The maximum size of a value you can store in memcached is 1 megabyte. memoize
# uses the function name and input variables as the key. flask-caching can also
# be used to cache view functions, templates and data explicitly.
# see https://flask-caching.readthedocs.io/en/latest/
@cache.memoize(timeout=30)
def get_customers():
    results = []

    conn = db_client.conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT name
        FROM customers
        ORDER BY name
    """)
    for row in cur:
        results.append(row)
    cur.close()

    return results
