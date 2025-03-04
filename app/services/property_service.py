from app.models.property import Property
from app.models.room import Room
from app import db

def create_property(name, description, type, city, owner_id):
    new_property = Property(
        name=name,
        description=description,
        type=type,
        city=city,
        owner_id=owner_id
    )
    db.session.add(new_property)
    db.session.commit()
    return new_property

def update_property(property_id, name=None, description=None, type=None, city=None):
    property = Property.query.get_or_404(property_id)

    if name:
        property.name = name
    if description:
        property.description = description
    if type:
        property.type = type
    if city:
        property.city = city

    db.session.commit()
    return property

def get_properties_by_city(city):
    return Property.query.filter_by(city=city).all()

def add_room_to_property(property_id, name, size):
    new_room = Room(
        name=name,
        size=size,
        property_id=property_id
    )
    db.session.add(new_room)
    db.session.commit()
    return new_room