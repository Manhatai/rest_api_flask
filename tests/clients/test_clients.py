from app import app # Flasks instance of the API
import json
from config.config import Config
import jwt
import pytest


def test_get_all_clients():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")
    
    response = app.test_client().get('/clients', headers=token_header)
    assert response.status_code == 200

    decode = response.data.decode('utf-8')
    response_count = json.loads(decode)
    assert type(response_count) is list
    assert len(response_count) > 0
    for client in response_count:
        assert type(client) is dict
        assert "id" in client
        assert "firstName" in client
        assert "phone" in client
        assert type(client["id"]) is int
        assert type(client["firstName"]) is str
        assert type(client["phone"]) is str


def test_get_single_client():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")
    response = app.test_client().get('/clients/1', headers=token_header)
    assert response.status_code == 200
    
    decode = response.data.decode('utf-8')
    client = json.loads(decode)

    assert type(client) is dict
    assert len(client) > 0
    assert "id" in client
    assert "firstName" in client
    assert "phone" in client
    assert type(client["id"]) is int
    assert type(client["firstName"]) is str
    assert type(client["phone"]) is str



def test_add_and_delete_client():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")


    new_client = {
        "firstName": "Test",
        "phone": "1234567890"
    }

    response = app.test_client().post('/clients', data=json.dumps(new_client), headers=token_header, content_type='application/json')
    decode = response.data.decode('utf-8')
    client = json.loads(decode)
    assert type(client) is dict
    assert "firstName" in client
    assert "phone" in client
    assert response.status_code == 201


    client_id = client["id"]
    cleanup_response = app.test_client().delete(f'/clients/{client_id}', headers=token_header)
    assert cleanup_response.status_code == 204


def test_empty_string_fail():
    with pytest.raises(Exception) as e_info:
        token = Config.LOCAL_TOKEN
        token_header = {
            'Authorize': token
        }
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except:
            print("Token invalid or expired")


        new_client = {
        "firstName": "",
        "phone": "1234567890"
        }  
        response = app.test_client().post('/clients', data=json.dumps(new_client), headers=token_header, content_type='application/json')
        assert response.status_code == 201