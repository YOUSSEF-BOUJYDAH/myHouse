from app import db

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)

    def __repr__(self):
        return f"<Room {self.name}>"