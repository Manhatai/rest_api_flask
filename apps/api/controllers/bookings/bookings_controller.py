from flask import jsonify, abort, request, Blueprint
from flask_restful import marshal_with, fields
from apps.api.controllers.cars import cars_controller
from apps.api.controllers.clients import clients_controller
from infra.sql.db.database import db
from infra.sql.clients.clients_model import ClientsModel
from infra.sql.cars.cars_model import CarsModel
from infra.sql.bookings.bookings_model import BookingsModel
from utils.logger.logger import logger
from utils.auth.authorization_check import authorization_required
from utils.catch.global_catch import global_catch

bookings_bp = Blueprint("bookings_handling", __name__)

resource_fields_bookings = { 
    'id': fields.Integer,
    'date': fields.String,
    'hour': fields.String,
    'car': fields.Nested(cars_controller.resource_fields_cars),       
    'client': fields.Nested(clients_controller.resource_fields_clients)    
}

@bookings_bp.route("/bookings/<int:booking_id>", methods=["GET"])
@global_catch
@marshal_with(resource_fields_bookings)
@authorization_required
def GetBooking(booking_id):
    booking = BookingsModel.query.filter_by(id=booking_id).first()
    if not booking:
        logger.info(f"Booking with id {booking_id} not found. [404]")
        abort(404, description="Booking with this id doesn't exists...")
    logger.info(f"GET request received for car {booking_id} succesfull. [200]") 
    return booking, 200

@bookings_bp.route("/bookings/<int:booking_id>", methods=["PUT"])
@global_catch
@marshal_with(resource_fields_bookings)
@authorization_required
def UpdateBooking(booking_id):
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
    return booking, 200

@bookings_bp.route("/bookings/<int:booking_id>", methods=["DELETE"])
@global_catch
@marshal_with(resource_fields_bookings)
@authorization_required
def DeleteBooking(booking_id):
    booking = BookingsModel.query.filter_by(id=booking_id).first()
    if booking == None:
        logger.info(f"Booking with id {booking_id} doesn't exist. [404]")
        abort(404, description="Booking with this id doesn't exists...")   
    db.session.delete(booking)
    db.session.commit()
    logger.info(f"Booking with id {booking_id} deleted successfully. [204]")
    return '', 204


@bookings_bp.route("/bookings", methods=["GET"])
@global_catch
@marshal_with(resource_fields_bookings)
@authorization_required
def GetBookingsList():
    bookings = BookingsModel.query.order_by(BookingsModel.id).all()
    logger.info(f"Booking list returned successfully. [200]")
    return bookings, 200

@bookings_bp.route("/bookings", methods=["POST"])
@global_catch
@marshal_with(resource_fields_bookings)
@authorization_required
def AddNewBooking():
    data = request.json
    if not data['date'] or not data['hour'] or not data["car_id"] or not data['client_id']:
        abort(400, description="Data cannot be empty!")
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
    return new_booking, 201