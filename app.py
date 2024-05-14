from flask import Flask, request         
from flask_restful import Api, Resource, reqparse

app = Flask(__name__) 
api = Api(app) 

cars = {
    "bmw1": {"brand": "bmw", "model": "e36", "year": 2013, "malfunction": "overheating"},
    "toyota1": {"brand": "toyota", "model": "supra", "year": 1996, "malfunction": "flat_tires"},
    "mitsubishi1": {"brand": "mitsubishi", "model": "lancer", "year": 2008, "malfunction": "dead_battery"},
    "skoda1": {"brand": "skoda", "model": "fabia", "year": 2018, "malfunction": "fuel_economy"},
    "ford1": {"brand": "ford", "model": "focus", "year": 2010, "malfunction": "steering"}
}

clients = {
    "mateusz": {"phone": 607962056, "firstName": "mateusz"},
    "tomasz": {"phone": 123456789, "firstName": "tomasz"},
    "andrzej": {"phone": 678234321, "firstName": "andrzej"},
    "krzysztof": {"phone": 890123435, "firstName": "krzysztof"},
    "szymon": {"phone": 796140911, "firstName": "szymon"}
}

booking = {
    "00023": {"date": "12.06.2024", "hour": "15:00"},
    "00046": {"date": "4.06.2024", "hour": "17:00"},
    "00133": {"date": "1.06.2024", "hour": "8:00"},
    "00067": {"date": "10.06.2024", "hour": "10:00"},
    "00089": {"date": "27.06.2024", "hour": "19:00"},
}

booking_put_args = reqparse.RequestParser() # Automatically parses through the request being sent (checks if it hass all necesary data)
booking_put_args.add_argument("date", type=str, help="Date of the new booking")
booking_put_args.add_argument("hour", type=str, help="Hour of the new booking")

class Clients(Resource): # Returns particular items
    def get(self, name): 
        return {name: clients[name]} # name == index
    
class Cars(Resource):
    def get(self, name): 
        return {name: cars[name]} 
    
class Booking(Resource):
    def get(self, name):
        return {name: booking[name]}
    
    def put(self, name):
        args = booking_put_args.parse_args() # Takes all the arguments probided by request parser
        return {name: args}



class ClientsList(Resource): # Returns lists of items
    def get(self): 
        return clients 
    
class CarsList(Resource):
    def get(self): 
        return cars
    
class BookingList(Resource):
    def get(self):
        return booking

        

api.add_resource(Clients, "/clients/<string:name>") # The endpoint is set to the clients first name
api.add_resource(Cars, "/cars/<string:name>")
api.add_resource(Booking, "/booking/<string:name>")


api.add_resource(ClientsList, "/clients")
api.add_resource(CarsList, "/cars")
api.add_resource(BookingList, "/booking")


if __name__ == "__main__":
    app.run(debug=True)


"""
    GET - a list of all planed repairs
    POST - adding to the repairs list
    DELETE - deleting from the repairs list
    PUT - updating the repairs list

Car:
- brand
- model
- year of production
- malfunction

Client:
- phone number
- name

Booking:
- date and hour
"""