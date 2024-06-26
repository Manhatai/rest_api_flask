from flask import jsonify, abort, request, Blueprint
from flask_restful import marshal_with, fields
from infra.sql.db.database import db
from infra.sql.cars.cars_model import CarsModel
from infra.sql.bookings.bookings_model import BookingsModel
from utils.logger.logger import logger
from utils.auth.authorization_check import authorization_required
from utils.catch.global_catch import global_catch

cars_bp = Blueprint("cars_handling", __name__)

resource_fields_cars = {
    'id': fields.Integer,
    'brand': fields.String,
    'model': fields.String,
    'year': fields.Integer,
    'malfunction': fields.String
}

@cars_bp.route("/cars/<int:car_id>", methods=["GET"])
@global_catch
@marshal_with(resource_fields_cars)
@authorization_required
def GetCar(car_id):
    car = CarsModel.query.filter_by(id = car_id).first()
    if not car:
        logger.info(f"Car with id {car_id} not found. [404]")
        abort(404, description="Car with this id doesn't exists...")  
    logger.info(f"GET request received for car {car_id} succesfull. [200]") 
    return car, 200

@cars_bp.route("/cars/<int:car_id>", methods=["PUT"])
@global_catch
@marshal_with(resource_fields_cars)
@authorization_required
def UpdateCar(car_id):
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
    return car, 200

@cars_bp.route("/cars/<int:car_id>", methods=["DELETE"])
@global_catch
@marshal_with(resource_fields_cars)
@authorization_required
def DeleteCar(car_id):
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

@cars_bp.route("/cars", methods=["GET"])
@global_catch
@marshal_with(resource_fields_cars)
@authorization_required
def GetCarsList():
    cars = CarsModel.query.order_by(CarsModel.id).all()
    logger.info(f"Car list returned successfully. [200]")
    return cars, 200
    # return jsonify([{'id': car.id, 'brand': car.brand, 'model': car.model, 'year': car.year, 'malfunction': car.malfunction} for car in cars]), 200

@cars_bp.route("/cars", methods=["POST"])
@global_catch
@marshal_with(resource_fields_cars)
@authorization_required
def AddNewCar():
    data = request.json
    new_car = CarsModel(brand=data['brand'], model=data['model'], year=data['year'], malfunction=data['malfunction'])
    if not data['brand'] or not data['model'] or not data['year'] or not data['malfunction']:
        abort(400, description="Data cannot be empty!")
    db.session.add(new_car) 
    db.session.commit() 
    logger.info(f"Client created with ID {new_car.id} successfully. [201]")
    return new_car, 201
    # return jsonify({'id': new_car.id, 'brand': new_car.brand, 'model': new_car.model, 'year': new_car.year, 'malfunction': new_car.malfunction}), 201 # 201 = CREATED 