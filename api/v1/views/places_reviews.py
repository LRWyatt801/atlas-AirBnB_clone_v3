#!/usr/bin/python3
"""Handles all default RESTful API actions for review objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews(place_id=None):
    """Retrieves list of all reviews for given place id

    Args:
        place_id (uuid): uuid for place linked to review objs

    Returns:
        json: Returns json list of all review objs for place if place_id given.
    """
    # Returns all review objs containing matching place_id
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    review_list = []
    for obj_key, review_obj in storage.all(Review).items():
        if review_obj.place_id == place_id:
            review_dict = review_obj.to_dict()
            review_list.append(review_dict)
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id=None):
    """Retrieves review for given review id

    Args:
        review_id (uuid): uuid for review obj

    Returns:
        json: Returns json for single review obj if review_id given.
    """
    # Returns one review obj matching review_id
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Deletes a review obj that matches given review_id

    Args:
        review_id (uuid): uuid of review obj

    Returns:
        dict: empty dictionary and Status:200 on success,
              otherwise abort(404)
    """
    if review_id:
        review_key = "Review." + review_id
        if review_key in storage.all():
            storage.all()[review_key].delete()
            storage.save()
            return jsonify({}), 200
    # Returns error if review_id doesn't match any objects
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id=None):
    """Creates review obj given provided json data

    Args:
        place_id (uuid): place id to be associated with new review

    Returns:
        new review obj based on json, place_id
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if "text" not in data:
        abort(400, description="Missing text")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    place_obj = storage.get(Place, place_id)
    user_obj = storage.get(User, data["user_id"])
    if not place_obj or not user_obj:
        abort(404)
    # add place_id to data dictionary to ensure it's passed to new review
    data["place_id"] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id=None):
    """Updates review obj given provided json data

    Args:
        review_id (uuid): id used to identify review obj

    Returns:
        updated review obj based on json
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
