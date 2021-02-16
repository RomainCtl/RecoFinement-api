import pytest
import json
from src.model import ProfileModel, GenreModel, ContentType
import uuid
from src import db


class TestProfile:
    ### GET PROFILE RESOURCE ###

    def test_profile_resource(self, test_client, headers_admin):
        """ Test profile get resource

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            200, {"profile": ProfileObject, "status" : True}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get(
            "/api/profile/"+str(profile.uuid), headers=headers_admin)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_profile_resource_bad_jwt(self, test_client, headers_bad):
        """Test profile get resource with bad access token

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get(
            "/api/profile/"+str(profile.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_resource_fake_jwt(self, test_client, headers_fake):
        """Test get profile resource with fake access token

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get(
            "/api/profile/"+str(profile.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_resource_no_jwt(self, test_client):
        """Test profile get resource without access token

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get("/api/profile/"+str(profile.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_resource_bad_uuid(self, test_client, headers_admin):
        """Test get profile resource with bad uuid

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            404, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        response = test_client.get(
            "/api/profile/"+str(uuid.uuid4()), headers=headers_admin)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### DELETE PROFILE ###

    def test_delete_profile_bad_jwt(self, test_client, headers_bad):
        """Test delete profile with bad access token

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_delete_profile_fake_jwt(self, test_client, headers_fake):
        """Test delete profile resource with fake access token

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            403, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_fake)
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 404
        assert res['status'] == False

    def test_delete_profile_no_jwt(self, test_client):
        """Test delete profile resource without access token

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete("/api/profile/"+str(profile.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_delete_profile_bad_uuid(self, test_client, headers_admin, admin_test2):
        """Test delete profile resource with bad uuid

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            403, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin2").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_admin)
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 404
        assert res['status'] == False

    def test_delete_profile_other_profile(self, test_client, headers_admin, admin_test2):
        """Test delete other profile resource with access token

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            403, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin2").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_admin)
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 404
        assert res['status'] == False

    def test_delete_profile(self, test_client, headers_admin):
        """ Test profile delete resource

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_admin)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    ### UPDATE PROFILE ###

    def test_update_profile(self, test_client, headers_admin):
        """ Test profile update resource

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers_admin, json=dict(
            profilename="admin2"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="admin2").first()

        assert response.status_code == 201
        assert res['status'] == True
        assert profile.profilename == "admin2"

    def test_update_profile_bad_jwt(self, test_client, headers_bad):
        """Test profile update with bad access token

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin2").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers_bad, json=dict(
            profilename="admin1"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="admin2").first()

        assert response.status_code == 422
        assert profile.profilename == "admin2"

    def test_update_profile_fake_jwt(self, test_client, headers_fake):
        """Test update profile resource with fake access token

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin2").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers_fake, json=dict(
            profilename="admin1"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="admin2").first()

        #assert res['message'] == "test"
        assert response.status_code == 404
        assert res['status'] == False
        assert profile.profilename == "admin2"

    def test_update_profile_no_jwt(self, test_client):
        """Test update profile resource without access token

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="admin2").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), json=dict(
            profilename="admin1"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="admin2").first()

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
        assert profile.profilename == "admin2"

    def test_update_profile_bad_uuid(self, test_client, headers_admin, admin_test2):
        """Test update profile resource with bad uuid

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            403, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin2").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers_admin, json=dict(
            profilename="admin1"
        ))
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 404
        assert res['status'] == False

    ### PROFILE GENRE ###

    def test_profile_genre(self, test_client, headers_admin):
        """Test get profile genres with access token

        Test:
            GET: /api/profile/<profile_uuid>/genre

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get(
            "/api/profile/"+str(profile.uuid)+"/genre", headers=headers_admin)
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 200
        assert res['status'] == True

    def test_profile_genre_bad_jwt(self, test_client, headers_bad):
        """Test profile genre with bad access token

        Test:
            GET: /api/profile/<profile_uuid>/genre

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get(
            "/api/profile/"+str(profile.uuid)+"/genre", headers=headers_bad)
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_genre_fake_jwt(self, test_client, headers_fake):
        """Test get profile genre with fake access token

        Test:
            GET: /api/profile/<profile_uuid>genre

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get(
            "/api/profile/"+str(profile.uuid)+"/genre", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_genre_not_jwt(self, test_client):
        """Test get profile genre without access token

        Test:
            GET: /api/profile/<profile_uuid>/genre

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.get("/api/profile/"+str(profile.uuid)+"/genre")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### PROFILE GENRE ID - UPDATE ###

    def test_profile_genre_id(self, test_client, headers_admin, genre_test1):
        """Test update profile genre by id with access token

        Test:
            PUT: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            201, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.put(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id), headers=headers_admin)
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 201
        assert res['status'] == True

    def test_profile_genre_id_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test update profile genre by id  with fake access token

        Test:
            PUT: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.put(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_genre_id_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test get profile genre id with bad access token

        Test:
            PUT: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.put(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_genre_id_no_jwt(self, test_client, genre_test1):
        """Test update profile genre by id without access token

        Test:
            PUT: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.put(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_genre_id_bad_id(self, test_client, headers_admin):
        """Test profile genre by bad id with access token

        Test:
            PUT: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.put(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(9999999), headers=headers_admin)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ###  PROFILE GENRE ID - DELETE ###

    def test_profile_genre_delete(self, test_client, headers_admin, genre_test1):
        """Test delete profile genre by id with access token

        Test:
            DELETE: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            201, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id), headers=headers_admin)
        res = json.loads(response.data)

        #assert res['message'] == "test"
        assert response.status_code == 201
        assert res['status'] == True

    def test_profile_genre_delete_id_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test delete profile genre by id with fake access token

        Test:
            DELETE: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_genre_delete_id_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test profile genre id delete with bad access token

        Test:
            DELETE: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id), headers=headers_bad)
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_genre_delete_id_no_jwt(self, test_client, genre_test1):
        """Test delete profile genre by id without access token

        Test:
            DELETE: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        #genre = GenreModel.query.filter_by(name="genre test").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(genre_test1.genre_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_genre_delete_id_bad_id(self, test_client, headers_admin):
        """Test delete profile genre by bad id with access token

        Test:
            DELETE: /api/profile/<profile_uuid>/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_admin (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="admin1").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid)+"/genre/"+str(9999999), headers=headers_admin)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
