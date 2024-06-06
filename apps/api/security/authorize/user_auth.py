from flask import jsonify, request, abort, Blueprint
import jwt
import datetime
from datetime import timedelta
import bcrypt
from infra.sql.users.users_model import UsersModel
from config.config import Config
from utils.logger.logger import logger
from utils.catch.global_catch import global_catch

authorize_bp = Blueprint("user_auth", __name__)

@authorize_bp.route("/authorize", methods=['POST'])
@global_catch
def UserAuth():
    try:
        data = request.json
        if not data.get('login'):
            abort(400, description="Login required!")
        if not data.get('password'):
            abort(400, description="Password required!")
        login = data.get('login')
        password = data.get('password')
        user = UsersModel.query.filter_by(login=login).first()
        if not user:
            abort(400, description="User with this login doesn't exist...")
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode('utf-8')): # user.password = hashed password, will return true if password is correct
            token = jwt.encode({'user': user.login, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.SECRET_KEY, algorithm='HS256') # HS256 = HMAC SHA256 header, user_login is the payload, secret_key is the signature.
            logger.info(f"Client with ID {user.id} logged in successfully. [200]")
            return jsonify({"token": token}), 200 
        else:               
            abort(400, description="Wrong password!")
    except:
        abort(400, description="Auth failed!")