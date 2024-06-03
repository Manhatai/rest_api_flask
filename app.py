from flask import Flask, jsonify, request, abort, make_response, render_template, session
# import jwt
# from datetime import datetime, timedelta
# from functools import wraps
from flask_sqlalchemy import SQLAlchemy
# from flask_restful import marshal_with, fields
from dotenv import load_dotenv
import os
import logging
import bcrypt

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

class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class AuthorizationService:

    def __init__(self):
        self.token = None

    def UserAuthorization(self):
        data = request.json
        if not data.get('login'):
            abort(400, description="Login required!")
        if not data.get('password'):
            abort(400, description="Password required!")
        login = data.get('login')
        password = data.get('password')
        user = UsersModel.query.filter_by(login=login).first()
        if not user:
            abort(400, description="User with this login doesn't exist...")
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode('utf-8')): # user.password = hashed password, will return true if password is correct
            token = 'token' + login
            self.token = token
            return jsonify({"token": token}), 200 
        else:               
            abort(400, description="Wrong password!")

    def AuthenticationCheck(self):
        if request.headers.get('Authorize') != self.token:
            abort(401, description="Unauthorized")

auth_service = AuthorizationService()


@app.route("/authorize", methods=['POST'])
def UserAuth():
    return auth_service.UserAuthorization()

@app.route("/authorize/register", methods=['POST'])
def RegisterUser():
    data = request.json
    if not data.get('login'):
        abort(400, description="Login required!")
    if not data.get('password'):
        abort(400, description="Password required!")
    login = data.get('login')
    password = data.get('password')
    potential_user = UsersModel.query.filter_by(login=login).first()
    if potential_user.login == login:
        abort(400, description="Login already exists!")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) # .encode for converting string into bytes
    new_user = UsersModel(login=login, password=hashed.decode('utf-8')) # .decode bytes back to string
    db.session.add(new_user)
    db.session.commit()
    logger.info(f"Client created with ID {new_user.id} successfully. [201]")
    return f'New user {login} created.', 201


@app.route("/clients/<int:client_id>", methods=["GET"])
def GetClient(client_id):
    auth_service.AuthenticationCheck()
    client = ClientsModel.query.filter_by(id = client_id).first() # Filters all of the clients in the database by id picking the first one to display (WITHOUT .first() IT ALWAYS RETURNS A NULL AND CAUSES AN ERROR!!!). Query - from SQL.
    if not client: # if not client: <=> if client == False: 
        logger.info(f"Client with id {client_id} not found. [404]")
        abort(404, description="Client with this id doesn't exists...")  # 404 = Not Found  
    logger.info(f"GET request for client {client_id} successfull. [200]") # Saves what happened with the server in logs.log - file
    return jsonify({'id': client.id, 'firstName': client.firstName, 'phone': client.phone}), 200


@app.route("/clients/<int:client_id>", methods=["PUT"])
def UpdateClient(client_id):
    auth_service.AuthenticationCheck()
    client = ClientsModel.query.filter_by(id = client_id).first()
    if not client:
        logger.info(f"Client with id {client_id} not found. [404]")
        abort(404, description="Client with this id doesn't exists...")
    data = request.json
    for key, value in data.items(): # .items() allows to iterate by both keys and values 
        setattr(client, key, value) # setattr very helpful while working with JSON's
    db.session.add(client)
    db.session.commit()
    logger.info(f"Client with id {client_id} updated successfully. [201]")
    return jsonify({'id': client.id, 'firstName': client.firstName, 'phone': client.phone}), 200


@app.route("/clients/<int:client_id>", methods=["DELETE"])
def DeleteClient(client_id):
    auth_service.AuthenticationCheck()
    client = ClientsModel.query.filter_by(id = client_id).first()
    if client == None:
        logger.info(f" Client with id {client_id} doesn't exist. [404]")
        abort(404, description="Client with this id doesn't exists...")
    booking_check = BookingsModel.query.filter_by(client_id = client_id).first()
    if booking_check != None:
        logger.info(f"Client {client_id} has a booking history. Deletion unsuccessfull. [409]")
    db.session.delete(client) # Deletes an entry
    db.session.commit()
    logger.info(f"Client with id {client_id} deleted successfully. [204]")
    return '', 204



@app.route("/cars/<int:car_id>", methods=["GET"])
def GetCar(car_id):
    auth_service.AuthenticationCheck()
    car = CarsModel.query.filter_by(id = car_id).first()
    if not car:
        logger.info(f"Car with id {car_id} not found. [404]")
        abort(404, description="Car with this id doesn't exists...")  
    logger.info(f"GET request received for car {car_id} succesfull. [200]") 
    return jsonify({'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year, 'malfunction': car.malfunction}), 200


@app.route("/cars/<int:car_id>", methods=["PUT"])
def UpdateCar(car_id):
    auth_service.AuthenticationCheck()
    car = CarsModel.query.filter_by(id = car_id).first()
    if car == None:
        logger.info(f"Car with id {car_id} doesn't exist. [404]")
        abort(404, description="Car with this id doesn't exists...")
    data = request.json
    for key, value in data.items(): 
        setattr(car, key, value) 
    db.session.add(car)
    db.session.commit()
    logger.info(f"Car with id {car_id} updated successfully. [201]")
    return jsonify({'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year, 'malfunction': car.malfunction}), 200
    

@app.route("/cars/<int:car_id>", methods=["DELETE"])
def DeleteCar(car_id):
    auth_service.AuthenticationCheck()
    car = CarsModel.query.filter_by(id = car_id).first()
    if car == None:
        logger.info(f"Car with id {car_id} doesn't exist. [404]")
        abort(404, description="Car with this id doesn't exists...")
    booking_check = BookingsModel.query.filter_by(car_id = car_id).first()
    if booking_check != None:
        logger.info(f" Car {car_id} has a booking history. Deletion unsuccessfull. [409]")
        abort(409, description="Client has a booking history! Delete booking history first to proceed...")
    db.session.delete(car)
    db.session.commit()
    logger.info(f"Car with id {car_id} deleted successfully. [204]")
    return '', 204



@app.route("/bookings/<int:booking_id>", methods=["GET"])
def GetBooking(booking_id):
    auth_service.AuthenticationCheck()
    booking = BookingsModel.query.filter_by(id=booking_id).first()
    if not booking:
        logger.info(f"Booking with id {booking_id} not found. [404]")
        abort(404, description="Booking with this id doesn't exists...")
    logger.info(f"GET request received for car {booking_id} succesfull. [200]") 
    return jsonify({
        'id': booking.id,
        'date': booking.date,
        'hour': booking.hour,
        'car': {
            'id': booking.car.id,
            'brand': booking.car.brand,
            'model': booking.car.model,
            'year': booking.car.year,
            'malfunction': booking.car.malfunction
            },
        'client': {
            'id': booking.client.id,
            'firstName': booking.client.firstName,
            'phone': booking.client.phone
            }
        }), 200

@app.route("/bookings/<int:booking_id>", methods=["PUT"])
def UpdateBooking(booking_id):
    auth_service.AuthenticationCheck()
    booking = BookingsModel.query.filter_by(id = booking_id).first()
    if booking == None:
        logger.info(f"Booking with id {booking_id} doesn't exist. [404]")
        abort(404, description="Booking with this id doesn't exists...")        
    print(booking)
    data = request.json
    for key, value in data.items(): 
        setattr(booking, key, value) 
    db.session.add(booking)
    db.session.commit() # Changing the client and its car in bookings table would be way too much effort as they are considered bidirectional data with 'cars' and 'clients' class, so in the end its easier to just change 'date' and 'hour' of the appointment.
    logger.info(f"Booking with id {booking_id} updated successfully. [201]")
    return jsonify({
        'id': booking.id,
        'date': booking.date,
        'hour': booking.hour,
        'car': {
            'id': booking.car.id,
            'brand': booking.car.brand,
            'model': booking.car.model,
            'year': booking.car.year,
            'malfunction': booking.car.malfunction
            },
        'client': {
            'id': booking.client.id,
            'firstName': booking.client.firstName,
            'phone': booking.client.phone
            }
        }), 200

@app.route("/bookings/<int:booking_id>", methods=["DELETE"])
def DeleteBooking(booking_id):
    auth_service.AuthenticationCheck()
    booking = BookingsModel.query.filter_by(id=booking_id).first()
    if booking == None:
        logger.info(f"Booking with id {booking_id} doesn't exist. [404]")
        abort(404, description="Booking with this id doesn't exists...")   
    db.session.delete(booking)
    db.session.commit()
    logger.info(f"Booking with id {booking_id} deleted successfully. [204]")
    return '', 204


@app.route("/clients", methods=["GET"])
def GetClientsList():
    auth_service.AuthenticationCheck()
    clients = ClientsModel.query.order_by(ClientsModel.id).all()
    logger.info(f"Client list returned successfully. [200]")
    return jsonify([{'id': client.id, 'firstName': client.firstName, 'phone': client.phone} for client in clients]), 200


@app.route("/clients", methods=["POST"])
def AddNewClient():
    auth_service.AuthenticationCheck()
    data = request.json
    new_client = ClientsModel(firstName=data['firstName'], phone=data['phone'])
    db.session.add(new_client) # Adds an object to a database
    db.session.commit() # Commits changes to the database
    logger.info(f"Client created with ID {new_client.id} successfully. [201]")
    return jsonify({'id': new_client.id, 'firstName': new_client.firstName, 'phone': new_client.phone}), 201 # 201 = CREATED 



@app.route("/cars", methods=["GET"])
def GetCarsList():
    auth_service.AuthenticationCheck()
    cars = CarsModel.query.order_by(CarsModel.id).all()
    logger.info(f"Car list returned successfully. [200]")
    return jsonify([{'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year, 'malfunction': car.malfunction} for car in cars]), 200

@app.route("/cars", methods=["POST"])
def AddNewCar():
    auth_service.AuthenticationCheck()
    data = request.json
    new_car = CarsModel(brand=data['brand'], model=data['model'], year=data['year'], malfunction=data['malfunction'])
    db.session.add(new_car) 
    db.session.commit() 
    logger.info(f"Client created with ID {new_car.id} successfully. [201]")
    return jsonify({'id': new_car.id, 'brand': new_car.brand, 'model': new_car.model, 'year': new_car.year, 'malfunction': new_car.malfunction}), 201 # 201 = CREATED 



@app.route("/bookings", methods=["GET"])
def GetBookingsList():
    auth_service.AuthenticationCheck()
    bookings = BookingsModel.query.order_by(BookingsModel.id).all()
    logger.info(f"Booking list returned successfully. [200]")
    return jsonify([{
        'id': booking.id,
        'date': booking.date,
        'hour': booking.hour,
        'car': {
            'id': booking.car.id,
            'brand': booking.car.brand,
            'model': booking.car.model,
            'year': booking.car.year,
            'malfunction': booking.car.malfunction
            },
        'client': {
            'id': booking.client.id,
            'firstName': booking.client.firstName,
            'phone': booking.client.phone
            }
        } for booking in bookings]), 200

@app.route("/bookings", methods=["POST"])
def AddNewBooking():
    auth_service.AuthenticationCheck()
    data = request.json
    car = CarsModel.query.filter_by(id=data['car_id']).first()
    if car == None:
        logger.info(f"Car with id {data['car_id']} not found. [404]")
        abort(404, message="Car with this id doesn't exists...")
    client = ClientsModel.query.filter_by(id=data['client_id']).first()
    if client == None:
        logger.info(f"Client with id {data['client_id']} not found. [404]")
        abort(404, message="Client with this id doesn't exists...")
    new_booking = BookingsModel(date=data['date'], hour=data['hour'], car_id=car.id, client_id=client.id)
    db.session.add(new_booking)
    db.session.commit()
    logger.info(f"Booking created successfully. [201]")
    return jsonify({
            'id': new_booking.id,
            'date': new_booking.date,
            'hour': new_booking.hour,
            'car': {
                'id': new_booking.car.id,
                'brand': new_booking.car.brand,
                'model': new_booking.car.model,
                'year': new_booking.car.year,
                'malfunction': new_booking.car.malfunction
            },
            'client': {
                'id': new_booking.client.id,
                'firstName': new_booking.client.firstName,
                'phone': new_booking.client.phone
            }
        }), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)