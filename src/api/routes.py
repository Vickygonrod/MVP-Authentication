"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, send_from_directory
from api.models import db, Walker, Owner, Dog
from api.utils import generate_sitemap, APIException


api = Blueprint('api', __name__)


###------------------------------------------------Walker Crud------------------------------------------------#




@api.route('/walkers', methods=['GET'])
def get_walkers():

    walkers = Walker.query.all()
    walkers_serialized = list(map(lambda x: x.serialize(), walkers))

    response_body = {
        'results': walkers_serialized
    }
    return jsonify(response_body), 200



@api.route('/walkers/<int:walker_id>', methods=['GET'])
def get_walker(walker_id):

    walker = Walker.query.get(walker_id)

    if walker_id < 1:
        raise APIException('El id no es válido', status_code=400)

    if walker == None:
        raise APIException('Este caminador no existe', status_code=400)

    response_body = {
        'results': walker.serialize()
    }
    return jsonify(response_body), 200


@api.route('/walkers/<int:walker_id>', methods=['PUT'])
def update_walker(walker_id):
    walker = Walker.query.get(walker_id)
    body = request.get_json()

    updatewalker = Walker.query.get(walker_id)

    if "first_name" in body:
        walker.first_name = body["first_name"]
    if "last_name" in body:
        walker.last_name = body["last_name"]
    if "username" in body:
        walker.username = body["username"]

    db.session.commit()

    response_body ={
        "message": "ok",
        "updateMsg": "User Updated.",
        "upadateowner": updatewalker.serialize()
    }
    return jsonify(response_body), 200





###------------------------------------------------Owner Crud------------------------------------------------#




@api.route('/owners', methods=['GET'])
def get_owners():

    owners = Owner.query.all()
    owners_serialized = list(map(lambda x: x.serialize(), owners))

    response_body = {
        'results': owners_serialized
    }
    return jsonify(response_body), 200

@api.route('/owners/<int:owner_id>', methods=['GET'])
def get_owner(owner_id):

    if owner_id < 1:
        raise APIException('El id no es válido', status_code=400)

    owner = Owner.query.get(owner_id)

    if owner == None:
        raise APIException('Este dueño no existe', status_code=400)

    response_body = {
        'results': owner.serialize()
    }
    return jsonify(response_body), 200

@api.route('/owners/<int:owner_id>', methods=['PUT'])
def put_owner_id(owner_id):
    body = request.get_json()

    updateowner = Owner.query.get(owner_id)

    if "first_name" in body:
        updateowner.first_name = body["first_name"]
    if "last_name" in body:
        updateowner.last_name = body["last_name"]
    if "username" in body:
        updateowner.username = body["username"]

    db.session.commit()

    response_body = {
        "message": "ok",
        "updateMsg": "User Updated.",
        "upadateowner": updateowner.serialize()
    }

    return jsonify(response_body), 200




###------------------------------------------------Dog Crud------------------------------------------------#





@api.route('/dogs', methods=['GET'])
def get_dogs():

    dogs = Dog.query.all()
    dogs_serialized = list(map(lambda x: x.serialize(), dogs))

    response_body = {
        'all_dogs': dogs_serialized
    }

    return jsonify(response_body), 200

@api.route('/dogs/<int:owner_id>', methods=['GET'])
def get_dog_id(owner_id):

    if owner_id < 1:
        raise APIException('El id no es válido', status_code=400)

    owner_dogs = Dog.query.filter_by(owner_id = owner_id)

    if owner_dogs is None:
        raise APIException('El dueño con ese id no tiene perros', status_code=400)

    dogs = list(map(lambda x: x.serialize(), owner_dogs))

    response_body = {
        "result": dogs
    }

    return jsonify(response_body), 200

@api.route('/dogs/<int:dog_id>', methods=['PUT'])
def put_dog_id(dog_id):
    body = request.get_json()

    updatedog = Dog.query.get(dog_id)

    if "name" in body:
        updatedog.name = body['name']
    if 'breed' in body:
        updatedog.breed = body['breed']
    if 'age' in body:
        updatedog.age = body['age']

    db.session.commit()

    response_body = {
        "message": "ok",
        "updateMsg": "Dog Updated.",
        "updatedog": updatedog.serialize()
    }

    return jsonify(response_body), 200