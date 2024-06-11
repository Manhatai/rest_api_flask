from app import app # Flasks instance of the API
import json
from config.config import Config
import jwt
import pytest


def test_get_all_cars():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")
    
    response = app.test_client().get('/cars', headers=token_header)
    assert response.status_code == 200

    decode = response.data.decode('utf-8')
    response_count = json.loads(decode)
    assert type(response_count) is list
    assert len(response_count) > 0
    for car in response_count:
        assert type(car) is dict
        assert "id" in car
        assert "brand" in car
        assert "model" in car
        assert "year" in car
        assert "malfunction" in car
        assert type(car["id"]) is int
        assert type(car["brand"]) is str
        assert type(car["model"]) is str
        assert type(car["year"]) is int
        assert type(car["malfunction"]) is str


def test_get_single_car():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")
    response = app.test_client().get('/cars/1', headers=token_header)
    assert response.status_code == 200
    
    decode = response.data.decode('utf-8')
    car = json.loads(decode)

    assert type(car) is dict
    assert "id" in car
    assert "brand" in car
    assert "model" in car
    assert "year" in car
    assert "malfunction" in car
    assert type(car["id"]) is int
    assert type(car["brand"]) is str
    assert type(car["model"]) is str
    assert type(car["year"]) is int
    assert type(car["malfunction"]) is str


def test_add_and_delete_car():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")


    new_car = {
	    "brand": "ford",
	    "model": "focus",
	    "year": 2010,
	    "malfunction": "steering"
    }

    response = app.test_client().post('/cars', data=json.dumps(new_car), headers=token_header, content_type='application/json')
    decode = response.data.decode('utf-8')
    car = json.loads(decode)
    assert type(car) is dict
    assert "id" in car
    assert "brand" in car
    assert "model" in car
    assert "year" in car
    assert "malfunction" in car
    assert response.status_code == 201


    car_id = car["id"]
    cleanup_response = app.test_client().delete(f'/cars/{car_id}', headers=token_header)
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


        new_car = {
            "brand": "ford",
            "model": "focus",
            "year": 2010,
            "malfunction": "steering"
        }
    
        response = app.test_client().post('/clients', data=json.dumps(new_car), headers=token_header, content_type='application/json')
        assert response.status_code == 201