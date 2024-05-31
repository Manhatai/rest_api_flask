from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging

load_dotenv()
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")

logging.basicConfig(filename="logs.log",
                    level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{login}:{password}@{host}/postgres'
db = SQLAlchemy(app)

class ClientsModel(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String, nullable=False)
    bookings = db.relationship('BookingsModel', back_populates='client')

class CarsModel(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand = db.Column(db.String(15), nullable=False)
    model = db.Column(db.String(15), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    malfunction = db.Column(db.String(40), nullable=False)
    bookings = db.relationship('BookingsModel', back_populates='car')

class BookingsModel(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(10), nullable=False)
    hour = db.Column(db.String(5), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    car = db.relationship('CarsModel', back_populates='bookings')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('ClientsModel', back_populates='bookings')


@app.route("/clients/<int:client_id>", methods=["GET", "PUT", "DELETE"])
def ClientsHandler():
    return '', 200


@app.route("/cars/<int:car_id>", methods=["GET", "PUT", "DELETE"])
def CarsHandler():
    return '', 200


@app.route("/bookings/<int:booking_id>", methods=["GET", "PUT", "DELETE"])
def BookingsHandler():
    return '', 200


@app.route("/clients", methods=["GET", "POST"])
def ClientsListHandler():
    return '', 200


@app.route("/cars", methods=["GET", "POST"])
def CarsListHandler():
    return '', 200


@app.route("/bookings", methods=["GET", "POST"])
def BookingsListHandler():
    return '', 200





if __name__ == "__main__":
    app.run(debug=True)