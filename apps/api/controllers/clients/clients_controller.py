from flask import jsonify, abort, request, Blueprint
from flask_restful import marshal_with, fields
from infra.sql.db.database import db
from infra.sql.clients.clients_model import ClientsModel
from infra.sql.bookings.bookings_model import BookingsModel
from utils.logger.logger import logger
from utils.auth.authorization_check import authorization_required
from utils.catch.global_catch import global_catch

clients_bp = Blueprint("clients_handling", __name__)

resource_fields_clients = {
    'id': fields.Integer,
    'firstName': fields.String,
    'phone': fields.String
}

@clients_bp.route("/clients/<int:client_id>", methods=["GET"])
@global_catch
@marshal_with(resource_fields_clients)
@authorization_required
def GetClient(client_id):
    # raise TypeError("Only integers are allowed") 
    client = ClientsModel.query.filter_by(id = client_id).first() # Filters all of the clients in the database by id picking the first one to display (WITHOUT .first() IT ALWAYS RETURNS A NULL AND CAUSES AN ERROR!!!). Query - from SQL.
    if not client: # if not client: <=> if client == False: 
        logger.info(f"Client with id {client_id} not found. [404]")
        abort(404, description="Client with this id doesn't exists...")  # 404 = Not Found  
    logger.info(f"GET request for client {client_id} successfull. [200]") # Saves what happened with the server in logs.log - file
    return client, 200
    # return jsonify({'id': client.id, 'firstName': client.firstName, 'phone': client.phone}), 200


@clients_bp.route("/clients/<int:client_id>", methods=["PUT"])
@global_catch
@marshal_with(resource_fields_clients)
@authorization_required
def UpdateClient(client_id):
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
    return client, 200
    # return jsonify({'id': client.id, 'firstName': client.firstName, 'phone': client.phone}), 200


@clients_bp.route("/clients/<int:client_id>", methods=["DELETE"])
@global_catch
@marshal_with(resource_fields_clients)
@authorization_required
def DeleteClient(client_id):
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

@clients_bp.route("/clients", methods=["POST"])
@global_catch
@marshal_with(resource_fields_clients)
@authorization_required
def AddNewClient():
    data = request.json
    new_client = ClientsModel(firstName=data['firstName'], phone=data['phone'])
    db.session.add(new_client) # Adds an object to a database
    db.session.commit() # Commits changes to the database
    logger.info(f"Client created with ID {new_client.id} successfully. [201]")
    return new_client, 200
    # return jsonify({'id': new_client.id, 'firstName': new_client.firstName, 'phone': new_client.phone}), 201 # 201 = CREATED 

@clients_bp.route("/clients", methods=["GET"])
@global_catch
@marshal_with(resource_fields_clients)
@authorization_required
def GetClientsList():
    clients = ClientsModel.query.order_by(ClientsModel.id).all()
    logger.info(f"Client list returned successfully. [200]")
    return clients, 200
    # return jsonify([{'id': client.id, 'firstName': client.firstName, 'phone': client.phone} for client in clients]), 200


