#!/usr/bin/python3
"""Handles all default RESTful API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


@app_views.route("/states", methods=["GET"])
@app_views.route("/states/<state_id>", methods=["GET"])
def get_states(state_id=None):
    """Retrieves state obj(s)

    Args:
        state_id (uuid, optional): uuid for state obj. Defaults to None.

    Returns:
        json: when no state_id is given returns json list of all state objs,
              when state_id is given and is found returns json state obj
              matching state_id, otherwise abort(404)
    """
    states_list = []
    all_states = storage.all(State)
    # Returns one state obj matching state_id
    if state_id:
        state_key = "State." + state_id
        if state_key in all_states:
            return jsonify(all_states[state_key].to_dict())
        else:
            return abort(404)
    # Returns all existing state objs
    for obj_key, state_object in all_states.items():
        state_dict = state_object.to_dict()
        states_list.append(state_dict)
    return jsonify(states_list)

@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_states(state_id):
    """Deletes an obj from storage

    Args:
        state_id (uuid): uuid of obj to delete

    Returns:
        dict: empty dictionary and code:200 on success,
              otherwise abort(404)
    """
    if state_id:
        state_key = "State." + state_id
        if state_key in storage.all():
            storage.all()[state_key].delete()
            storage.save()
            return jsonify({}), 200
    abort(404)