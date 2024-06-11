from app import app # Flasks instance of the API
from config.config import Config
import jwt


def test_get_img():

    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")

    response = app.test_client().get('/web/index.html', headers=token_header)
    assert response.status_code == 200