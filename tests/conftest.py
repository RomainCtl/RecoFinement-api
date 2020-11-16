from flask_jwt_extended import create_access_token
import pytest

from src import create_app


@pytest.fixture(scope="function")
def headers():
    access_token = create_access_token(identity="f27da1ab-e045-4883-9b80-206d01335e7e")
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
