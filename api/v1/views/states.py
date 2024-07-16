#!/usr/bin/python3
"""Handles all default RESTful API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"])
@app_views.route("/states/<state_id>", methods=["GET"])
def get_states(state_id=None):
    """Handles all API actions

    Args:
        state_id (uuid, optional): uuid for state obj. Defaults to None.

    Returns:
        json: when no state_id is given returns json list of all state objs,
              when state_id is given and is found returns json state obj
              matching state_id, otherwise abort(404)
    """
    # Returns one state obj matching state_id
    if state_id:
        state_obj = storage.get(State, state_id)
        if not state_obj:
            abort(404)
        return jsonify(state_obj.to_dict())
    # Returns all existing state objs
    states_list = []
    for obj_key, state_object in storage.all(State).items():
        state_dict = state_object.to_dict()
        states_list.append(state_dict)
    return jsonify(states_list)

@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Deletes a state object that matchs by state_id

    Args:
        state_id (uuid): uuid of state object

    Returns:
        dict: empty dictionary and Status:200 on success,
              otherwise abort(404)
    """
    if state_id:
        state_key = "State." + state_id
        if state_key in storage.all():
            storage.all()[state_key].delete()
            storage.save()
            return jsonify({}), 200
    # if state_id doesn't match any objects, return 404
    abort(404)

@app_views.route("/states", methods=["POST"])
@app_views.route("/states/<state_id>", methods=["PUT"])
def create_state(state_id=None):
    # get JSON
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    # state_id given, update existing state obj
    if state_id:
        state_obj = storage.get(State, state_id)
        if not state_obj:
            abort(404)
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state_obj, key, value)
        storage.save()
        return jsonify(state_obj.to_dict()), 200
    # state_id not given, create new state obj
    if "name" not in data:
        abort(400, description="Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
