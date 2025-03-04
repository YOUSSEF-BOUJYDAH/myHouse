from app import db

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rooms = db.relationship('Room', backref='property', lazy=True)

    def __repr__(self):
        return f"<Property {self.name}>"