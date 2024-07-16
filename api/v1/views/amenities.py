#!/usr/bin/python3
"""Handles all default RESTful API actions for Amenity objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenities(amenity_id=None):
    """Retrieves Amenity object(s)

    Args:
        amenity_id (uuid, optional): uuid for amenity obj

    Returns:
        json: Returns single amenity obj if amenity_id given.
              Returns json list of all amenity objs otherwise.
    """
    # Returns one amenity obj matching amenity_id
    if amenity_id:
        amenity_obj = storage.get(Amenity, amenity_id)
        if not amenity_obj:
            abort(404)
        return jsonify(amenity_obj.to_dict())
    # Returns all existing amenity objs
    amenities_list = []
    for obj_key, amenity_object in storage.all(Amenity).items():
        amenity_dict = amenity_object.to_dict()
        amenities_list.append(amenity_dict)
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes a amenity obj that matches given amenity_id

    Args:
        amenity_id (uuid): uuid of amenity obj

    Returns:
        dict: empty dictionary and Status:200 on success,
              otherwise abort(404)
    """
    if amenity_id:
        amenity_key = "Amenity." + amenity_id
        if amenity_key in storage.all():
            storage.all()[amenity_key].delete()
            storage.save()
            return jsonify({}), 200
    # Returns error if amenity_id doesn't match any objects
    abort(404)


@app_views.route("/amenities", methods=["POST"])
@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def create_amenity(amenity_id=None):
    """Creates and/or updates amenity objects

    Args:
        amenity_id (uuid, optional): uuid for a specific amenity object.
                                     Defaults to None.

    Returns:
        JSON: recently created/updated amenity object
    """
    # get JSON
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    # amenity_id given, update existing amenity obj
    if amenity_id:
        amenity_obj = storage.get(Amenity, amenity_id)
        if not amenity_obj:
            abort(404)
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity_obj, key, value)
        storage.save()
        return jsonify(amenity_obj.to_dict()), 200
    if "name" not in data:
        abort(400, description="Missing name")
    # amenity_id not given, create new amenity obj
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201
