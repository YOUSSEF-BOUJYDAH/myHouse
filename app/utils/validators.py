from app.models.property import Property

def validate_ownership(property_id, user_id):

    property = Property.query.get(property_id)
    if property and property.owner_id == user_id:
        return True
    return False