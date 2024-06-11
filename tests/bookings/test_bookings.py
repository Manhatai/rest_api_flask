from app import app # Flasks instance of the API
import json
from config.config import Config
import jwt
import pytest


def test_get_all_bookings():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")
    
    response = app.test_client().get('/bookings', headers=token_header)
    assert response.status_code == 200

    decode = response.data.decode('utf-8')
    response_count = json.loads(decode)
    assert type(response_count) is list
    assert len(response_count) > 0
    for booking in response_count:
        assert type(booking) is dict
        assert "id" in booking
        assert "date" in booking
        assert "hour" in booking
        assert "client" in booking
        assert "car" in booking
        assert type(booking["id"]) is int
        assert type(booking["date"]) is str
        assert type(booking["hour"]) is str
        assert type(booking["client"]) is dict
        assert type(booking["car"]) is dict



def test_get_single_booking():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")
    response = app.test_client().get('/bookings/1', headers=token_header)
    assert response.status_code == 200
    
    decode = response.data.decode('utf-8')
    booking = json.loads(decode)

    assert type(booking) is dict
    assert "id" in booking
    assert "date" in booking
    assert "hour" in booking
    assert "client" in booking
    assert "car" in booking
    assert type(booking["id"]) is int
    assert type(booking["date"]) is str
    assert type(booking["hour"]) is str
    assert type(booking["client"]) is dict
    assert type(booking["car"]) is dict



def test_add_and_delete_booking():
    token = Config.LOCAL_TOKEN
    token_header = {
        'Authorize': token
    }
    try:
        jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    except:
        print("Token invalid or expired")


    new_booking = {
	    "date": "29.06.2024",
	    "hour": "20:00",
	    "car_id": 1,
	    "client_id": 1
    }


    response = app.test_client().post('/bookings', data=json.dumps(new_booking), headers=token_header, content_type='application/json')
    decode = response.data.decode('utf-8')
    booking = json.loads(decode)
    assert type(booking) is dict
    assert "id" in booking
    assert "date" in booking
    assert "hour" in booking
    assert "client" in booking
    assert "car" in booking
    assert response.status_code == 201


    booking_id = booking["id"]
    cleanup_response = app.test_client().delete(f'/bookings/{booking_id}', headers=token_header)
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


        new_booking = {
            "date": "29.06.2024",
            "hour": "20:00",
            "car_id": 1,
            "client_id": 1
        }
        response = app.test_client().post('/clients', data=json.dumps(new_booking), headers=token_header, content_type='application/json')
        assert response.status_code == 201