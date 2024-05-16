# Same as app.py, just with a database (about to be) included.
from flask import Flask         
from flask_restful import Api, Resource, reqparse, fields, marshal_with #abort (WIP)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 
api = Api(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workshop.db' # Database name and location, same directiory as script
db = SQLAlchemy(app) # Same as above, wrapping app


class ClientsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key = unique identifier
    firstName = db.Column(db.String)
    phone = db.Column(db.Integer, nullable=False) # Can't be null 

    def __repr__(self):
        return f"Clients(firstName={firstName}, phone={phone})"



clients_put_args = reqparse.RequestParser() # Automatically parses through the request being sent (checks if it hass all necesary data)
clients_put_args.add_argument( "firstName", type=str, help="Clients first name is required.", required=True )
clients_put_args.add_argument( "phone", type=int, help="Phone number is required.", required=True           )

cars_put_args = reqparse.RequestParser() 
cars_put_args.add_argument( "brand", type=str, help="Brand name is required.", required=True             )
cars_put_args.add_argument( "model", type=str, help="Model name is required.", required=True             )
cars_put_args.add_argument( "year", type=int, help="Production year is required.", required=True         )
cars_put_args.add_argument( "malfunction", type=str, help="Malfunction type is required.", required=True )

bookings_put_args = reqparse.RequestParser()
bookings_put_args.add_argument( "id", type=int, help="ID of the new booking is required.", required=True     )
bookings_put_args.add_argument( "date", type=str, help="Date of the new booking is required.", required=True )
bookings_put_args.add_argument( "hour", type=str, help="Hour of the new booking is required.", required=True )

resource_fields = { # Making a dictionary that defines fields from the database model
    'id': fields.Integer,
    'firstName': fields.String,
    'phone': fields.Integer
}
  
# Get specific elements from an array
class Clients(Resource): 

    @marshal_with(resource_fields) # Takes the resource value we get from result and serializes it by resource_fields, making it easy to read
    def get(self, client_id):
        result = ClientsModel.query.filter_by(id = client_id).first() # Filters all of the clients in the database by id, outputs the first one only (id's are unique)
        return result
    
    @marshal_with(resource_fields)
    def post(self, client_id): 
        args = clients_put_args.parse_args()
        client = ClientsModel(id=client_id, firstName=args['firstName'], phone=args['phone'])

        db.session.add(client) # Adds an object to a database session
        db.session.commit() # Commits changes to the session
        return client, 201 # 201 = CREATED message
    
    @marshal_with(resource_fields)
    def delete(self, client_id):
        del clients[client_id] # Deletes an entry with x id
        return f'Item with id {client_id} deleted from clients list', 204
    
    # A post method prooved to be completely redundant, as put can do the exact same thing.
    
class Cars(Resource):
    def get(self, car_id): 
        return cars[car_id]
    
    def put(self, car_id):
        args = cars_put_args.parse_args() 
        cars[car_id] = args
        return cars[car_id], 201
    
    def delete(self, car_id):
        del cars[car_id]
        return f'Item with id {car_id} deleted from cars list', 204
    
class Bookings(Resource):
    def get(self, booking_id):
        return bookings[booking_id]
    
    def put(self, booking_id):
        args = bookings_put_args.parse_args()
        bookings[booking_id] = args
        return bookings[booking_id], 201
    
    def delete(self, booking_id):
        del bookings[booking_id]
        return f'Item with id {booking_id} deleted from bookings list', 204

# Get item lists
class ClientsList(Resource): # Returns lists of items
    def get(self): 
        return clients 
    
class CarsList(Resource):
    def get(self): 
        return cars
    
class BookingList(Resource):
    def get(self):
        return bookings


# Defining endpoints
api.add_resource(Clients, "/clients/<int:client_id>") # The endpoint is set to the id essentialy beeing an input id
api.add_resource(Cars, "/cars/<int:car_id>")
api.add_resource(Bookings, "/bookings/<int:booking_id>")


api.add_resource(ClientsList, "/clients")
api.add_resource(CarsList, "/cars")
api.add_resource(BookingList, "/bookings")


if __name__ == "__main__":
    app.run(debug=True)