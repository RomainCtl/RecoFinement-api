import pytest
import json
from src.model import UserModel
from src import db
from flask_jwt_extended import create_access_token
import uuid


class TestAuth:

    ### REGISTER ###
    def test_register(self, test_client):
        """test user registration

        Test:
            POST: /api/auth/register

        Expected result:
            201, {"content": UserObject, "status" : True}

        Args:
            test_client (app context): Flask application
        """
        if (user := UserModel.query.filter_by(username="test").first()):
            UserModel.query.filter_by(username="test").delete()
            db.session.commit()
        response = test_client.post('/api/auth/register', json=dict(
            email="test@test.com",
            username="test",
            password="goodPassword!123"
        ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['user']['email'] == "test@test.com"
        assert res['status'] == True

    def test_register_email_exist(self, test_client):
        """test user registration with already used email

        Test:
            POST: /api/auth/register

        Expected result:
            400, {"status" : False}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post('/api/auth/register', json=dict(
            email="test@test.com",
            username="test",
            password="goodPassword!123"
        ))
        res = json.loads(response.data)

        assert response.status_code == 400
        assert res['status'] == False

    ### LOGIN ###
    def test_login_ok(self, test_client):
        """test user login

        Test:
            POST: /api/auth/login

        Expected result:
            200, {"content": UserObject, "status" : True}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post("/api/auth/login", json=dict(
            email="test@test.com",
            password="goodPassword!123"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['user']['email'] == "test@test.com"

    def test_login_wrong_passd(self, test_client):
        """test user login with wrong password

        Test:
            POST: /api/auth/login

        Expected result:
            401, {"status" : False}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post(
            "/api/auth/login", json=dict(email="test@test.com", password="wrongPassword*"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['status'] == False

    def test_login_bad_email(self, test_client):
        """test user login with wrong email

        Test:
            POST: /api/auth/login

        Expected result:
            401, {"status" : False}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post(
            "/api/auth/login", json=dict(email="failure@test.com", password="wrongPassword*"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['status'] == False

    ### LOGOUT ###
    def test_logout(self, test_client, headers):
        """test user logout 

        Test:
            POST: /api/auth/logout

        Expected result:
            204, b''

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post('/api/auth/logout', headers=headers)
        res = response.data

        assert response.status_code == 204
        assert res == b''

    def test_logout_no_jwt(self, test_client):
        """test user logout whitout the token access

        Test:
            POST: /api/auth/logout

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post('/api/auth/logout')
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### FORGET PASSWORD ###

    def test_forget_passwd(self, test_client):
        """test user forgot password

        Test:
            POST: /api/auth/forgot

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post(
            '/api/auth/forget', json=dict(email="test@test.com"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_forget_passwd_bad_email(self, test_client):
        """test user forgot password bad email

        Test:
            POST: /api/auth/forgot

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post(
            '/api/auth/forget', json=dict(email="notest@test.com"))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    ### RESET PASSWORD ###

    def test_reset_passwd(self, test_client, user_test1):
        """test user reset password

        Test:
            POST: /api/auth/reset

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post('/api/auth/reset', json=dict(
            reset_password_token=create_access_token(identity=user_test1),
            password="Azerty!123"
        ))
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_reset_passwd_bad_token(self, test_client):
        """test user reset password bad token

        Test:
            POST: /api/auth/reset

        Expected result:
            401, {"status" : False}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.post('/api/auth/reset', json=dict(
            reset_password_token=str(
                create_access_token(identity=uuid.uuid4())),
            password="Azerty!123"))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['status'] == False
