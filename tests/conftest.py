from flask_jwt_extended import create_access_token
from py.xml import html
import pytest
import uuid

import settings.testing
from src import create_app, db
from src.model import UserModel, ProfileModel, GroupModel, GenreModel, ContentType, RoleModel, PermissionModel


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
    if hasattr(report, 'description'):
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
def user_role():
    if (role := RoleModel.query.filter_by(role_id=1).first()):
        return role
    else:
        indicate_interest = PermissionModel(
            permission="indicate_interest"
        )
        modify_user_profil = PermissionModel(
            permission="modify_user_profil"
        )
        view_recommendation = PermissionModel(
            permission="view_recommendation"
        )
        play_music = PermissionModel(
            permission="play_music"
        )
        add_content = PermissionModel(
            permission="add_content"
        )
        role = RoleModel(
            role_id=1,
            name="user",
            permission=[indicate_interest, modify_user_profil,
                        view_recommendation, play_music, add_content]
        )
        db.session.add(role)
        db.session.commit()
        return role


@pytest.fixture(scope="function")
def user_test1(user_role):
    """ create UserObject test1 & profile test1

    Returns:
        UserObject: user "test1"
    """
    if (user := UserModel.query.filter_by(username="test").first()):
        if not (ProfileModel.query.filter_by(profilename="test").first()):
            user = UserModel.query.filter_by(username="test").first()
            new_profile = ProfileModel(
                profilename="test",
                user_id=user.user_id
            )
            db.session.add(new_profile)
            db.session.commit()
        return user
    else:
        new_user = UserModel(
            email="test@test.com",
            username="test",
            password="goodPassword!123",
            role=[user_role]
        )
        db.session.add(new_user)
        db.session.commit()
        if not (ProfileModel.query.filter_by(profilename="test").first()):
            user = UserModel.query.filter_by(username="test").first()
            new_profile = ProfileModel(
                profilename="test",
                user_id=user.user_id
            )
            db.session.add(new_profile)
            db.session.commit()
        return new_user


@pytest.fixture(scope="function")
def user_test2(user_role):
    """ create UserObject test2 & profile test2

    Returns:
        UserObject: user "test2"
    """
    if (user := UserModel.query.filter_by(username="test2").first()):
        if not (ProfileModel.query.filter_by(profilename="test2").first()):
            user = UserModel.query.filter_by(username="test2").first()
            new_profile = ProfileModel(
                profilename="test2",
                user_id=user.user_id
            )
            db.session.add(new_profile)
            db.session.commit()
        return user
    else:
        new_user = UserModel(
            email="test2@test.com",
            username="test2",
            password="goodPassword!123",
            role=[user_role]
        )
        db.session.add(new_user)
        db.session.commit()
        if not (ProfileModel.query.filter_by(profilename="test2").first()):
            user = UserModel.query.filter_by(username="test2").first()
            new_profile = ProfileModel(
                profilename="test2",
                user_id=user.user_id
            )
            db.session.add(new_profile)
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
    access_token = create_access_token(identity=user_test1)
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
    fake_user = UserModel(uuid=uuid.uuid4())
    access_token = str(create_access_token(identity=fake_user))
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
