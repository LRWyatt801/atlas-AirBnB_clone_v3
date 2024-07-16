#!/usr/bin/python3
"""Handles all default RESTful API actions for user objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
@app_views.route("/users/<user_id>", methods=["GET"])
def get_users(user_id=None):
    """Retrieves user object(s)

    Args:
        user_id (uuid, optional): uuid for user obj

    Returns:
        json: Returns single user obj if user_id given.
              Returns json list of all user objs otherwise.
    """
    # Returns one user obj matching user_id
    if user_id:
        user_obj = storage.get(User, user_id)
        if not user_obj:
            abort(404)
        return jsonify(user_obj.to_dict())
    # Returns all existing user objs
    users_list = []
    for obj_key, user_object in storage.all(User).items():
        user_dict = user_object.to_dict()
        users_list.append(user_dict)
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a user obj that matches given user_id

    Args:
        user_id (uuid): uuid of user obj

    Returns:
        dict: empty dictionary and Status:200 on success,
              otherwise abort(404)
    """
    user_key = "user." + user_id
    if user_key in storage.all():
        storage.all()[user_key].delete()
        storage.save()
        return jsonify({}), 200
    # Returns error if user_id doesn't match any objects
    abort(404)


@app_views.route("/users", methods=["POST"])
@app_views.route("/users/<user_id>", methods=["PUT"])
def create_user(user_id=None):
    """Creates and/or updates user objects

    Args:
        user_id (uuid, optional): uuid for a specific user object.
                                  Defaults to None.

    Returns:
        JSON: recently created/updated user object
    """
    # get JSON
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    # user_id given, update existing user obj
    if user_id:
        user_obj = storage.get(User, user_id)
        if not user_obj:
            abort(404)
        for key, value in data.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user_obj, key, value)
        storage.save()
        return jsonify(user_obj.to_dict()), 200
    if "name" not in data:
        abort(400, description="Missing name")
    if "password" not in data:
        abort(400, description="Missing password")
    # user_id not given, create new user obj
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201
