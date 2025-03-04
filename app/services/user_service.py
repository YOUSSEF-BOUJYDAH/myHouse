from app.models.user import User
from app import db

def create_user(first_name, last_name, email, password, date_of_birth):
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        date_of_birth=date_of_birth
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_user(user_id, first_name=None, last_name=None, date_of_birth=None):
    user = User.query.get_or_404(user_id)
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if date_of_birth:
        user.date_of_birth = date_of_birth
    db.session.commit()
    return user