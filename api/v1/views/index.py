#!/usr/bin/python3

"""defines status route"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route("/status")
def status():
    response = {"status": "OK"}
    return jsonify(response)

@app_views.route("/stats")
def stats():
    response = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City), 
        "places": storage.count(Place), 
        "reviews": storage.count(Review), 
        "states": storage.count(State), 
        "users": storage.count(User)
    }
    return jsonify(response)