from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # En production, hachez le mot de passe
    date_of_birth = db.Column(db.String(10), nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"