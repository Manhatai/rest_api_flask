from flask import Flask         
from flask_restful import Api, Resource, reqparse #abort? (wip)

app = Flask(__name__) 
api = Api(app) 


clients = {
    0: { "firstName": "mateusz", "phone": 607962056   },
    1: { "firstName": "tomasz", "phone": 123456789    },
    2: { "firstName": "andrzej", "phone": 678234321   },
    3: { "firstName": "krzysztof", "phone": 890123435 },
    4: { "firstName": "szymon", "phone": 796140911    }
}

cars = {
    0: { "brand": "bmw", "model": "e36", "year": 2013, "malfunction": "overheating"            },
    1: { "brand": "toyota", "model": "supra", "year": 1996, "malfunction": "flat_tires"        },
    2: { "brand": "mitsubishi", "model": "lancer", "year": 2008, "malfunction": "dead_battery" },
    3: { "brand": "skoda", "model": "fabia", "year": 2018, "malfunction": "fuel_economy"       },
    4: { "brand": "ford", "model": "focus", "year": 2010, "malfunction": "steering"            }
}

bookings = {
    0: { "id": 23, "date": "12.06.2024", "hour": "15:00", "car": cars[0], 'client': clients[0] },
    1: { "id": 46, "date": "4.06.2024", "hour": "17:00", "car": cars[1], 'client': clients[1]  },
    2: { "id": 133, "date": "1.06.2024", "hour": "8:00", "car": cars[2], 'client': clients[2]  },
    3: { "id": 67, "date": "10.06.2024", "hour": "10:00", "car": cars[3], 'client': clients[3] },
    4: { "id": 89, "date": "27.06.2024", "hour": "19:00", "car": cars[4], 'client': clients[4] },
}


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

  
# Get specific elements from an array
class Clients(Resource): 
    def get(self, client_id):
        return clients[client_id] # Returns particular items based on the id provided
    
    def put(self, client_id): #
        args = clients_put_args.parse_args() # Takes all the arguments provided by request parser
        clients[client_id] = args # Updates or creates an entry based on the values provided
        return clients[client_id], 201 # 201 = CREATED message
    
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