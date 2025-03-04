from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import authenticate_user

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = authenticate_user(email, password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad email or password"}), 401