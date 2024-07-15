#!/usr/bin/python3

"""defines the function api_status"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_db(exception=None):
    storage.close()

@app.errorhandler(404)
def not_found(e):
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == "__main__":
    # hostname/port assigned env variable if it exists
    host_name = getenv("HBNB_API_HOST") or "0.0.0.0"
    port_number = int(getenv("HBNB_API_PORT") or 5000)

    app.run(host=host_name, port=port_number, threaded=True)
