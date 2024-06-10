from flask import Flask
from infra.sql.db.database import db
from config.config import Config
from apps.api.security.authorize.user_auth import authorize_bp
from apps.api.security.authorize.user_reg import register_bp
from apps.api.controllers.clients.clients_controller import clients_bp
from apps.api.controllers.cars.cars_controller import cars_bp
from apps.api.controllers.bookings.bookings_controller import bookings_bp
from apps.api.controllers.web.web_controller import web_bp
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(authorize_bp)
app.register_blueprint(register_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(cars_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(web_bp)


if __name__ == "__main__":
    if Config.REST_API_ENV_NAME.lower() == 'local':
        app.run(debug=Config.IS_DEBUG)
    else:
        app.run(ssl_context='adhoc', debug=Config.IS_DEBUG)