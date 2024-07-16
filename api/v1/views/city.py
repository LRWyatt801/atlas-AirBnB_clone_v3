#!/usr/bin/python3
"""Handles all default RESTful API actions for City objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id=None):
    """Retrieves list of all cities for given state id

    Args:
        state_id (uuid): uuid for state linked to city objs

    Returns:
        json: Returns json list of all city objs for state if state_id given.
    """
    # Returns all city objs containing matching state_id
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    city_list = []
    for obj_key, city_obj in storage.all(City).items():
        if city_obj.state_id == state_id:
            city_dict = city_obj.to_dict()
            city_list.append(city_dict)
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id=None):
    """Retrieves city for given city id

    Args:
        city_id (uuid): uuid for city obj

    Returns:
        json: Returns json for single city obj if city_id given.
    """
    # Returns one city obj matching city_id
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a city obj that matches given city_id

    Args:
        city_id (uuid): uuid of city obj

    Returns:
        dict: empty dictionary and Status:200 on success,
              otherwise abort(404)
    """
    if city_id:
        city_key = "City." + city_id
        if city_key in storage.all():
            storage.all()[city_key].delete()
            storage.save()
            return jsonify({}), 200
    # Returns error if city_id doesn't match any objects
    abort(404)

@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id=None):
    """Creates city obj given provided json data

    Args:
        state_id (uuid): state id to be associated with new city

    Returns:
        new city obj based on json, state_id
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    # add state_id to data dictionary to ensure it's passed to new city
    data["state_id"] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id=None):
    """Updates city obj given provided json data

    Args:
        city_id (uuid): id used to identify city obj

    Returns:
        updated city obj based on json
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    # state_id given, update existing state obj
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
