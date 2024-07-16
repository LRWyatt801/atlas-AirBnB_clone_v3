#!/usr/bin/python3
"""Handles all default RESTful API actions for place objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places(city_id=None):
    """Retrieves list of all places for given city id

    Args:
        city_id (uuid): uuid for city linked to place objs

    Returns:
        json: Returns json list of all place objs for city if city_id given.
    """
    # Returns all place objs containing matching city_id
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    place_list = []
    for obj_key, place_obj in storage.all(Place).items():
        if place_obj.city_id == city_id:
            place_dict = place_obj.to_dict()
            place_list.append(place_dict)
    return jsonify(place_list)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id=None):
    """Retrieves place for given place id

    Args:
        place_id (uuid): uuid for place obj

    Returns:
        json: Returns json for single place obj if place_id given.
    """
    # Returns one place obj matching place_id
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a place obj that matches given place_id

    Args:
        place_id (uuid): uuid of place obj

    Returns:
        dict: empty dictionary and Status:200 on success,
              otherwise abort(404)
    """
    if place_id:
        place_key = "Place." + place_id
        if place_key in storage.all():
            storage.all()[place_key].delete()
            storage.save()
            return jsonify({}), 200
    # Returns error if place_id doesn't match any objects
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id=None):
    """Creates place obj given provided json data

    Args:
        city_id (uuid): city id to be associated with new place

    Returns:
        new place obj based on json, city_id
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    city_obj = storage.get(City, city_id)
    user_obj = storage.get(User, data["user_id"])
    if not city_obj or not user_obj:
        abort(404)
    # add city_id to data dictionary to ensure it's passed to new place
    data["city_id"] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id=None):
    """Updates place obj given provided json data

    Args:
        place_id (uuid): id used to identify place obj

    Returns:
        updated place obj based on json
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict()), 200
