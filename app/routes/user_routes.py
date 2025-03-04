from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import create_user, update_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/add', methods=['POST'])
def register_user():
    data = request.get_json()
    user = create_user(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data['password'],  # En production, hachez le mot de passe
        date_of_birth=data['date_of_birth']
    )
    return jsonify({"message": "User created successfully", "user_id": user.id}), 201

@user_routes.route('/update/<int:user_id>', methods=['PUT'])
@jwt_required()
def modify_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"msg": "You can only update your own profile"}), 403

    data = request.get_json()
    updated_user = update_user(
        user_id=user_id,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=data.get('date_of_birth')
    )
    return jsonify({"message": "User updated successfully", "user": updated_user}), 200