#!/usr/bin/python3
"""Handles all default RESTful API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route("/states", methods=["GET"])
@app_views.route("/states/<state_id>", methods=["GET"])
def states(state_id=None):
    states_list = []
    all_states = storage.all(State)
    if state_id:
        state_key = "State." + state_id
        if state_key in all_states:
            return jsonify(all_states[state_key].to_dict())
        else:
            return abort(404)
    for obj_key, state_object in all_states.items():
        state_dict = state_object.to_dict()
        states_list.append(state_dict)
    return jsonify(states_list)
    