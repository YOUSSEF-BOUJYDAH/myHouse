from app.models.property import Property

def validate_ownership(property_id, user_id):
    """
    Vérifie si l'utilisateur est le propriétaire du bien.
    :param property_id: ID du bien
    :param user_id: ID de l'utilisateur
    :return: True si l'utilisateur est le propriétaire, False sinon
    """
    property = Property.query.get(property_id)
    if property and property.owner_id == user_id:
        return True
    return False