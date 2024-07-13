#!/usr/bin/python3

"""defines status route"""

from api.v1.views import app_views

@app_views.route("/status")
def status():
    # TODO - Make json-y
    return {"status":"OK"}
