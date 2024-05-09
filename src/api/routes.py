"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Vehicle, FavoriteVehicle, MyVehicleInRent
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager 

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_exist = User.query.filter_by(email=email).first()
    if user_exist is None: 
        new_user = User(
            email=email, 
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "User has already exist"}), 400

@api.route('/user/rent', methods=['GET'])
def get_all_rents():
    email =  get_jwt_identity()
    user_exist = User.query.filter_by(email=email).first()
    user_id = user_exist.id
    all_rents = MyVehicleInRent.query.filter_by(user_id=user_id).all()
    all_rents_list = list(map(lambda item: item.serialize(), all_rents))

    if all_rents_list == []:
        return jsonify({"msg":"You don't have vehicles in rent"}), 404

    response_body = {
        "msg": "ok",
        "results": [
            all_rents_list,
        ]
    }    
    return jsonify(response_body), 200