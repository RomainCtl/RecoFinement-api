from flask_jwt_extended import create_access_token
import pytest

from src import create_app, db
from src.model import UserModel


@pytest.fixture(scope="function")
def first_user():
    return UserModel.query.first()


@pytest.fixture(scope="function")
def headers(first_user):
    access_token = create_access_token(identity=first_user.uuid)
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
