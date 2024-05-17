# Same as app.py, just with a database included.
from flask import Flask         
from flask_restful import Api, Resource, reqparse, fields, marshal_with #abort - for specialized error messages (WIP)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) 
api = Api(app) # Initializes app with Api extension
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workshop.db' # Database name and location, same directiory as script
db = SQLAlchemy(app) # Same as above


class ClientsModel(db.Model): # Basically a database table
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True) # Primary key = unique identifier
    firstName = db.Column(db.String)
    phone = db.Column(db.Integer, nullable=False) # nullable=False = Can't be null
    bookings = db.relationship('BookingsModel', back_populates='client') # Defines a relationship to 'BookingsModel'. Could have called it bookings_relation, but it would require resetting the entire database.

class CarsModel(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True) 
    brand = db.Column(db.String, nullable=False)
    model = db.Column(db.String) 
    year = db.Column(db.String)
    malfunction = db.Column(db.String, nullable=False)
    bookings = db.relationship('BookingsModel', back_populates='car')

class BookingsModel(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    hour = db.Column(db.String, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    car = db.relationship('CarsModel', back_populates='bookings')
    client = db.relationship('ClientsModel', back_populates='bookings')


clients_put_args = reqparse.RequestParser() # Automatically parses through the request being sent (checks if it hass all necesary data)
clients_put_args.add_argument( "firstName", type=str)
clients_put_args.add_argument( "phone", type=int, help="Phone number is required.", required=True )

resource_fields_clients = { # Making a dictionary that defines fields from the database model, helping to serialize it (for'marshal_with').
    'id': fields.Integer,
    'firstName': fields.String,
    'phone': fields.Integer
}

cars_put_args = reqparse.RequestParser() 
cars_put_args.add_argument( "brand", type=str, help="Brand name is required.", required=True )
cars_put_args.add_argument( "model", type=str )
cars_put_args.add_argument( "year", type=int )
cars_put_args.add_argument( "malfunction", type=str, help="Malfunction type is required.", required=True )

resource_fields_cars = { # Making a dictionary that defines fields from the database model, helping to serialize it
    'id': fields.Integer,
    'brand': fields.String,
    'model': fields.String,
    'year': fields.Integer,
    'malfunction': fields.String
}

bookings_put_args = reqparse.RequestParser()
bookings_put_args.add_argument( "date", type=str, help="Date of the new booking is required.", required=True )
bookings_put_args.add_argument( "hour", type=str, help="Hour of the new booking is required.", required=True )
bookings_put_args.add_argument( "car_id", type=int, help="Car's id is required.", required=True )
bookings_put_args.add_argument( "client_id", type=int, help="Client's id is required.", required=True )

resource_fields_bookings = { # Making a dictionary that defines fields from the database model, helping to serialize it
    'id': fields.Integer,
    'date': fields.String,
    'hour': fields.String,
    'car': fields.Nested(resource_fields_cars),         # By taking in car or client id during post method execution, the resource field automatically nests 
    'client': fields.Nested(resource_fields_clients)    # data from other resource fields to display it properly in the database. Magic!
}

  
class Clients(Resource): 

    @marshal_with(resource_fields_clients) # Takes the resource value we get from result and serializes it by resource_fields, making it easy to read for the database. Very important!
    def get(self, client_id):
        client = ClientsModel.query.filter_by(id = client_id).first() # Filters all of the clients in the database by id picking the first one to display (WITHOUT .first() IT ALWAYS RETURNS A NULL AND CAUSES AN ERROR!!!). Query - from SQL.
        return client, 200
    
    @marshal_with(resource_fields_clients)
    def post(self, client_id): 
        args = clients_put_args.parse_args()
        client = ClientsModel(id=client_id, firstName=args['firstName'], phone=args['phone'])
        db.session.add(client) # Adds an object to a database
        db.session.commit() # Commits changes to the database
        return client, 201 # 201 = CREATED 
    
    @marshal_with(resource_fields_clients)
    def put(self, client_id):
        client = ClientsModel.query.filter_by(id = client_id).first()
        args = clients_put_args.parse_args()
        if 'firstName' in args:
            client.firstName = args['firstName'] # I should optimize it somehow (A loop that iterates through all args and queried variables)
        if 'phone' in args:
            client.phone = args['phone']
        db.session.add(client)
        db.session.commit()
        return client, 201
    
    @marshal_with(resource_fields_clients)
    def delete(self, client_id):
        client = ClientsModel.query.filter_by(id = client_id).first()
        db.session.delete(client) # Deletes an entry
        db.session.commit()
        return '', 410 # 410 = GONE
    
    
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
            car.brand = args['brand'] # I should optimize it somehow (A loop that iterates through all the arguments)
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

    @marshal_with(resource_fields_bookings)
    def get(self, booking_id):
        booking = BookingsModel.query.filter_by(id=booking_id).first()
        return booking, 200
    
    @marshal_with(resource_fields_bookings)
    def post(self, booking_id):
        args = bookings_put_args.parse_args()
        car = CarsModel.query.filter_by(id=args['car_id']).first() # Takes the car/client id the user provided and 
        client = ClientsModel.query.filter_by(id=args['client_id']).first()
        booking = BookingsModel(id=booking_id, date=args['date'], hour=args['hour'], car_id=car.id, client_id=client.id) # car_id=car.id checks if car's/client's id proviced by user is present in the database. If its not, the request returns an "AtributeError".
        db.session.add(booking)
        db.session.commit()
        return booking, 201
    
    @marshal_with(resource_fields_bookings)
    def put(self, booking_id):
        booking = BookingsModel.query.filter_by(id = booking_id).first()
        print(booking)
        args = bookings_put_args.parse_args()
        if 'date' in args:
            booking.date = args['date']
        if 'hour' in args:
            booking.hour = args['hour']
        db.session.add(booking)
        db.session.commit() # Changing the client and its car in bookings table would be way too much effort as they are considered bidirectional data with 'cars' and 'clients' class, so in the end its easier to just change 'date' and 'hour' of the appointment.
        return booking, 201

    @marshal_with(resource_fields_bookings)
    def delete(self, booking_id):
        booking = BookingsModel.query.filter_by(id=booking_id).first()
        db.session.delete(booking)
        db.session.commit()
        return '', 410

        
# Get item lists

class ClientsList(Resource): # Returns a list of items

    @marshal_with(resource_fields_clients)
    def get(self): 
        clients = ClientsModel.query.all() # query.all() = display all the elements from the table
        return clients
    
class CarsList(Resource):
    @marshal_with(resource_fields_cars)
    def get(self): 
        cars = CarsModel.query.all()
        return cars
    
class BookingList(Resource):
    @marshal_with(resource_fields_bookings)
    def get(self):
        bookings = BookingsModel.query.all()
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