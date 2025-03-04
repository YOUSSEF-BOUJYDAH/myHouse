from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.property_service import (
    create_property,
    update_property,
    get_properties_by_city,
    add_room_to_property
)

property_routes = Blueprint('property_routes', __name__)

@property_routes.route('/properties', methods=['POST'])
@jwt_required()
def add_property():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_property = create_property(
        name=data['name'],
        description=data.get('description'),
        type=data['type'],
        city=data['city'],
        owner_id=current_user_id
    )
    return jsonify({"message": "Property created successfully", "property_id": new_property.id}), 201

@property_routes.route('/properties/<int:property_id>', methods=['PUT'])
@jwt_required()
def modify_property(property_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    updated_property = update_property(
        property_id=property_id,
        owner_id=current_user_id,
        name=data.get('name'),
        description=data.get('description'),
        type=data.get('type'),
        city=data.get('city')
    )
    return jsonify({"message": "Property updated successfully", "property": updated_property}), 200

@property_routes.route('/properties/<string:city>', methods=['GET'])
def get_properties(city):
    properties = get_properties_by_city(city)
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "type": p.type,
        "city": p.city
    } for p in properties]), 200

@property_routes.route('/properties/<int:property_id>/rooms', methods=['POST'])
@jwt_required()
def add_room(property_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_room = add_room_to_property(
        property_id=property_id,
        owner_id=current_user_id,
        name=data['name'],
        size=data['size']
    )
    return jsonify({"message": "Room added successfully", "room_id": new_room.id}), 201