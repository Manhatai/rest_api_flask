from flask import Flask
from infra.sql.db.database import db
from config.config import Config
from apps.api.security.authorize.user_auth import authorize_bp
from apps.api.security.authorize.user_reg import register_bp
from apps.api.controllers.clients.clients_controller import clients_bp
from apps.api.controllers.cars.cars_controller import cars_bp
from apps.api.controllers.bookings.bookings_controller import bookings_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(authorize_bp)
app.register_blueprint(register_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(cars_bp)
app.register_blueprint(bookings_bp)

if __name__ == "__main__":
    app.run(debug=Config.IS_DEBUG)
