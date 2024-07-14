#!/usr/bin/python3

"""defines status route"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    response = {"status":"OK"}
    return jsonify(response)
