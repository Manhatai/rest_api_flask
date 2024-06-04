from flask import request, abort, Blueprint
from datetime import timedelta
import bcrypt
from infra.sql.users.users_model import UsersModel
from infra.sql.database import db
from utils.logger.logger import logger

register_bp = Blueprint("user_reg", __name__)

@register_bp.route("/authorize/register", methods=['POST'])
def RegisterUser():
    data = request.json
    if not data.get('login'):
        abort(400, description="Login required!")
    if not data.get('password'):
        abort(400, description="Password required!")
    login = data.get('login')
    password = data.get('password')
    potential_user = UsersModel.query.filter_by(login=login).first()
    if potential_user == None:
        pass
    else:
        if potential_user.login == login:
            abort(400, description="Login already exists!")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) # .encode for converting string into bytes
    new_user = UsersModel(login=login, password=hashed.decode('utf-8')) # .decode bytes back to string
    db.session.add(new_user)
    db.session.commit()
    logger.info(f"Client created with ID {new_user.id} successfully. [201]")
    return f'New user {login} created.', 201