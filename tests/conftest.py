from flask_jwt_extended import create_access_token
from py.xml import html
import pytest
import uuid

import settings.testing
from src import create_app, db
from src.model import UserModel, GroupModel, GenreModel, ContentType


def pytest_html_report_title(report):
    report.title = "Recofinement tests result"


def pytest_html_results_summary(prefix, summary, postfix):
    l = html.p(html.b("Coverage details: "))
    l.append(html.a("here", href="./coverage/index.html"))
    prefix.append(l)


def pytest_html_results_table_header(cells):
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = html.pre(item.function.__doc__)


def pytest_html_results_table_html(report, data):
    data.insert(0, report.description)


@pytest.fixture(scope="function")
def genre_test1():
    if (genre := GenreModel.query.filter_by(name="genre_test").first()):
        return genre
    else:
        new_genre = GenreModel(
            name="genre_test",
            count=0,
            content_type=ContentType.BOOK
        )
        db.session.add(new_genre)
        db.session.flush()
        db.session.commit()
        return new_genre


@pytest.fixture(scope="function")
def user_test1():
    """ create UserObject test1

    Returns:
        UserObject: user "test1"
    """
    if (user := UserModel.query.filter_by(username="test").first()):

        return user
    else:
        new_user = UserModel(
            email="test@test.com",
            username="test",
            password="goodPassword!123"
        )
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return new_user


@pytest.fixture(scope="function")
def user_test2():
    """ create UserObject test1

    Returns:
        UserObject: user "test1"
    """
    if (user := UserModel.query.filter_by(username="test2").first()):
        return user
    else:
        new_user = UserModel(
            email="test2@test.com",
            username="test2",
            password="goodPassword!123"
        )
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return new_user


@pytest.fixture(scope="function")
def group_test(user_test2):
    if (group := GroupModel.query.filter_by(name="group_test").first()):
        return group
    else:
        new_group = GroupModel(
            name="group_test",
            owner=user_test2
        )
        db.session.add(new_group)
        db.session.flush()
        db.session.commit()
        return new_group


@pytest.fixture(scope="function")
def group_test2(user_test2):
    if (group := GroupModel.query.filter_by(name="group_test2").first()):
        return group
    else:
        new_group = GroupModel(
            name="group_test2",
            owner=user_test2
        )
        db.session.add(new_group)
        db.session.flush()
        db.session.commit()
        return new_group


@pytest.fixture(scope="function")
def headers(user_test1):
    """Create header with access token from user test 1

    Args:
        user_test1 (UserObject): user "test1"

    Returns:
        Dict: Headers with the token access
    """
    access_token = create_access_token(identity=user_test1.uuid)
    return {
        "Authorization": "Bearer %s" % access_token
    }


@pytest.fixture(scope="function")
def headers_bad():
    """Create header with bad access token. It is a uuid

    Returns:
        Dict: Headers with the bad token access
    """
    access_token = str(uuid.uuid4())
    return {
        "Authorization": "Bearer %s" % access_token
    }


@pytest.fixture(scope="function")
def headers_fake():
    """Create header with fake access token signed by Flask application

    Returns:
        Dict: Headers with the fake token access
    """
    access_token = str(create_access_token(identity=uuid.uuid4()))
    return {
        "Authorization": "Bearer %s" % access_token
    }


@pytest.fixture(scope="module")
def test_client():
    """ The Flask test application

    Yields:
        [app context]: app context for the Flask test application
    """
    flask_app = create_app(settings.testing)

    # Flask provides a way to test your application exposing the Werkzeug test Client and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests
    ctx = flask_app.app_context()
    ctx.push()

    # Create db
    db.create_all()

    yield testing_client

    # Drop db
    db.drop_all()

    ctx.pop()