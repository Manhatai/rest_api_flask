from infra.sql.db.database import db

class ClientsModel(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String, nullable=False)
    bookings = db.relationship('BookingsModel', back_populates='client')