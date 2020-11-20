from flask_jwt_extended import create_access_token
import pytest
from py.xml import html
import uuid

from src import create_app, db
from src.model import UserModel


def pytest_html_report_title(report):
    report.title = "Recofinement tests result"

@pytest.fixture(scope="function")
def user_test1():
    if (user :=  UserModel.query.filter_by(username = "test").first()):
        return user
    else :
        new_user = UserModel(
                email= "test@test.com",
                username= "test",
                password = "goodPassword!123"
            )
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return new_user

@pytest.fixture(scope="function")
def user_test2():
    if (user :=  UserModel.query.filter_by(username = "test2").first()):
        return user
    else :
        new_user = UserModel(
                email= "test2@test.com",
                username= "test2",
                password = "goodPassword!123"
            )
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return new_user

@pytest.fixture(scope="function")
def headers(user_test1):
    access_token = create_access_token(identity=user_test1.uuid)
    return {
        "Authorization": "Bearer %s" % access_token
    }

@pytest.fixture(scope="function")
def headers_bad():
    access_token = str(uuid.uuid4())
    return {
        "Authorization": "Bearer %s" % access_token
    }

@pytest.fixture(scope="function")
def headers_fake():
    access_token = str(create_access_token(identity=uuid.uuid4()))
    return {
        "Authorization": "Bearer %s" % access_token
    }

@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    # Flask provides a way to test your application exposing the Werkzeug test Client and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()
