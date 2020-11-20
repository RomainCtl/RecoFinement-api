import pytest
import json
from src.model import UserModel
from src import db

class TestAuth:
    
    ### REGISTER ###
    def test_register(self,test_client):
        if ( user :=  UserModel.query.filter_by(username = "test").first()):
            UserModel.query.filter_by(username = "test").delete()
            db.session.commit()
        response = test_client.post('/api/auth/register', json=dict(
            email= "test@test.com",
            username= "test",
            password = "goodPassword!123"
        ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['user']['email'] == "test@test.com"
        assert res['status'] == True

    def test_register_email_exist(self,test_client):
        response = test_client.post('/api/auth/register', json=dict(
            email= "test@test.com",
            username= "test",
            password = "goodPassword!123"
        ))
        res = json.loads(response.data)

        assert response.status_code == 400
        assert res['status'] == False

    ### LOGIN ###
    def test_login_ok(self, test_client):
        response = test_client.post("/api/auth/login", json=dict(
            email="test@test.com",
            password="goodPassword!123"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['user']['email'] == "test@test.com"
    
    def test_login_wrong_passd(self, test_client):
        response = test_client.post("/api/auth/login", json=dict(email="test@test.com", password="wrongPassword*"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['status'] == False

    def test_login_bad_email(self, test_client):
        response = test_client.post("/api/auth/login", json=dict(email="failure@test.com", password="wrongPassword*"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['status'] == False

    ### LOGOUT ###
    def test_logout(self,test_client, headers):
        response = test_client.post('/api/auth/logout', headers=headers)
        res = response.data

        assert response.status_code == 204
        assert res == b''

    def test_logout_no_jwt(self,test_client, headers):
        response = test_client.post('/api/auth/logout')
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header" 

    def test_forget_passwd(self,test_client):
        response = test_client.post('/api/auth/forget', json=dict(email="test@test.com"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_forget_passwd_bad_email(self,test_client):
        response = test_client.post('/api/auth/forget', json=dict(email="notest@test.com"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
