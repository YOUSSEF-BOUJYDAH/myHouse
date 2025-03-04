from app.models.user import User
from app import db

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return user
    return None