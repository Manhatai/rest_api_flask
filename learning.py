# The goal is to create a basic Flask-RESTful API

from flask import Flask             
from flask_restful import Api, Resource


app = Flask(__name__) # Base code when creating a Flask app
api = Api(app) # Wraps the app as an API

names = {"mateusz": {"age": 21, "gender": "male"},
         "tomasz": {"age": 45, "gender": "male"}}

class HelloWorld(Resource): # What it is, is a Class that is a Resource. The resource will have a bunch of different methods that handle requests.
    def get(self, name): # Defines what happens when a get request is sent to a certain URL
        return names[name] # Represents a JSON format


api.add_resource(HelloWorld, "/helloworld/<string:name>") # Registering the class to api as a resource with an "/helloworld" endpoint


if __name__ == "__main__": # When python runs a script, it sets __name__ to __main__
    app.run(debug=True) # Used to run the development server in debug mode (remove debug for production)
