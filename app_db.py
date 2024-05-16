# Same as app.py, just with a database (about to be) included.
from flask import Flask         
from flask_restful import Api, Resource, reqparse, fields, marshal_with #abort (WIP)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 
api = Api(app) # Initializes app with Api extension
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workshop.db' # Database name and location, same directiory as script
db = SQLAlchemy(app) # Same as above

class ClientsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key = unique identifier
    firstName = db.Column(db.String)
    phone = db.Column(db.Integer, nullable=False) # nullable=False = Can't be null

class CarsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Primary key = unique identifier
    brand = db.Column(db.String, nullable=False)
    model = db.Column(db.String) # nullable=False = Can't be null
    year = db.Column(db.String)
    malfunction = db.Column(db.String)

##############################
# BOOKINGS MODEL PLACEHOLDER #
##############################

clients_put_args = reqparse.RequestParser() # Automatically parses through the request being sent (checks if it hass all necesary data)
clients_put_args.add_argument( "firstName", type=str, help="Clients first name is required.", required=True )
clients_put_args.add_argument( "phone", type=int, help="Phone number is required.", required=True           )

resource_fields_clients = { # Making a dictionary that defines fields from the database model, helping to serialize it
    'id': fields.Integer,
    'firstName': fields.String,
    'phone': fields.Integer
}

cars_put_args = reqparse.RequestParser() 
cars_put_args.add_argument( "brand", type=str, help="Brand name is required.", required=True             )
cars_put_args.add_argument( "model", type=str, help="Model name is required.", required=True             )
cars_put_args.add_argument( "year", type=int, help="Production year is required.", required=True         )
cars_put_args.add_argument( "malfunction", type=str, help="Malfunction type is required.", required=True )

resource_fields_cars = { # Making a dictionary that defines fields from the database model, helping to serialize it
    'id': fields.Integer,
    'brand': fields.String,
    'model': fields.String,
    'year': fields.Integer,
    'malfunction': fields.String
}

bookings_put_args = reqparse.RequestParser()
bookings_put_args.add_argument( "id", type=int, help="ID of the new booking is required.", required=True     )
bookings_put_args.add_argument( "date", type=str, help="Date of the new booking is required.", required=True )
bookings_put_args.add_argument( "hour", type=str, help="Hour of the new booking is required.", required=True )

#######################################
# BOOKINGS RESOURCE FIELD PLACEHOLDER #
#######################################
  
# Get specific elements from an array
class Clients(Resource): 

    @marshal_with(resource_fields_clients) # Takes the resource value we get from result and serializes it by resource_fields, making it easy to read for the database. Very important!
    def get(self, client_id):
        client = ClientsModel.query.filter_by(id = client_id).first() # Filters all of the clients in the database by id, outputs the first one only (id's are unique)
        return client, 200
    
    @marshal_with(resource_fields_clients)
    def post(self, client_id): 
        args = clients_put_args.parse_args()
        client = ClientsModel(id=client_id, firstName=args['firstName'], phone=args['phone'])
        db.session.add(client) # Adds an object to a database session
        db.session.commit() # Commits changes to the session
        return client, 201 # 201 = CREATED message
    
    @marshal_with(resource_fields_clients)
    def put(self, client_id):
        client = ClientsModel.query.filter_by(id = client_id).first()
        args = clients_put_args.parse_args()
        if 'firstName' in args:
            client.firstName = args['firstName'] # I should optimize it somehow?
        if 'phone' in args:
            client.phone = args['phone']
        db.session.add(client)
        db.session.commit()
        return client, 201
    
    @marshal_with(resource_fields_clients)
    def delete(self, client_id):
        client = ClientsModel.query.filter_by(id = client_id).first()
        db.session.delete(client)# Deletes an entry with x id
        db.session.commit()
        return '', 410 # 410 = gone
    
    
class Cars(Resource):

    @marshal_with(resource_fields_cars)
    def get(self, car_id): 
        car = CarsModel.query.filter_by(id = car_id).first()
        return car, 200
    
    @marshal_with(resource_fields_cars)
    def post(self, car_id):
        args = cars_put_args.parse_args()
        car = CarsModel(id=car_id, brand=args['brand'], model=args['model'], year=args['year'], malfunction=args['malfunction'])
        db.session.add(car)
        db.session.commit()
        return car, 201 
    
    @marshal_with(resource_fields_cars)
    def put(self, car_id):
        car = CarsModel.query.filter_by(id = car_id).first()
        args = cars_put_args.parse_args()
        if 'brand' in args:
            car.brand = args['brand'] # I should optimize it somehow?
        if 'model' in args:
            car.model = args['model']
        if 'year' in args:
            car.year = args['year']
        if 'malfunction' in args:
            car.malfunction = args['malfunction']
        db.session.add(car)
        db.session.commit()
        return car, 201
    
    @marshal_with(resource_fields_cars)
    def delete(self, car_id):
        car = CarsModel.query.filter_by(id = car_id).first()
        db.session.delete(car)
        db.session.commit()
        return '', 410
    
class Bookings(Resource):
    def get(self, booking_id):
        return bookings[booking_id], 200
    
    def post(self, booking_id):
        args = bookings_put_args.parse_args()
        bookings[booking_id] = args
        return bookings[booking_id], 201
    
    def delete(self, booking_id):
        del bookings[booking_id]
        return '', 410

# Get item lists

class ClientsList(Resource): # Returns lists of items

    @marshal_with(resource_fields_clients)
    def get(self): 
        clients = ClientsModel.query.all()
        return clients
    
class CarsList(Resource):
    
    @marshal_with(resource_fields_cars)
    def get(self): 
        cars = CarsModel.query.all()
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
    with app.app_context():
        db.create_all()
        app.run(debug=True)