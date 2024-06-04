from flask import Flask
from infra.sql.database import db
from config.config import Config
from apps.api.security.authorize.user_auth import authorize_bp
from apps.api.security.authorize.user_reg import register_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(authorize_bp)
app.register_blueprint(register_bp)

if __name__ == "__main__":
    app.run(debug=True)