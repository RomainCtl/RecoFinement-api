import pytest
import json
from src.model import ProfileModel, GenreModel, ContentType
import uuid
from src import db


class TestProfile:
    ### GET PROFILE RESOURCE ###

    def test_profile_resource(self, test_client, headers):
        """ Test profile get resource

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            200, {"profile": ProfileObject, "status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        assert profile.profilename == "test"
        response = test_client.get(
            "/api/profile/"+str(profile.uuid), headers=headers)
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
        profile = ProfileModel.query.filter_by(profilename="test").first()
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
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
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
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.get("/api/profile/"+str(profile.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_resource_bad_uuid(self, test_client, headers):
        """Test get profile resource with bad uuid

        Test:
            GET: /api/profile/<uuid>

        Expected result:
            404, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.get(
            "/api/profile/"+str(uuid.uuid4()), headers=headers)
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
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_delete_profile_fake_jwt(self, test_client, headers_fake):
        """Test delete profile resource with fake access token

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 403
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
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.delete("/api/profile/"+str(profile.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_delete_profile_bad_uuid(self, test_client, headers, profile_test2):
        """Test delete profile resource with bad uuid

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            403, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.delete(
            "/api/profile/"+str(profile_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False

    def test_delete_profile_other_profile(self, test_client, headers, profile_test2):
        """Test delete other profile resource with access token

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            403, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the access token
        """
        response = test_client.delete(
            "/api/profile/"+str(profile_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False

    def test_delete_profile(self, test_client, headers):
        """ Test profile delete resource

        Test:
            DELETE: /api/profile/<uuid>

        Expected result:
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.delete(
            "/api/profile/"+str(profile.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    ### UPDATE PROFILE ###

    def test_update_profile(self, test_client, headers):
        """ Test profile update resource

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers, json=dict(
            profilename="profile"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="test").first()

        assert response.status_code == 201
        assert res['status'] == True
        assert profile.profilename == "profile"

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
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers_bad, json=dict(
            profilename="profile"
        ))
        res = json.loads(response.data)

        assert response.status_code == 422
        assert profile.profilename == "profile"

    def test_update_profile_fake_jwt(self, test_client, headers_fake):
        """Test update profile resource with fake access token

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers_fake, json=dict(
            profilename="test"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="test").first()

        assert response.status_code == 403
        assert res['status'] == False
        assert profile.profilename == "profile"

    def test_update_profile_no_jwt(self, test_client):
        """Test update profile resource without access token

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), json=dict(
            profilename="test"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="test").first()

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
        assert profile.profilename == "profile"

    def test_update_profile_bad_uuid(self, test_client, headers, profile_test2):
        """Test update profile resource with bad uuid

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            403, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.patch("/api/profile/"+str(profile_test2.uuid), headers=headers, json=dict(
            profile="test"
        ))
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False

    def test_update_profile_bad_field(self, test_client, headers):
        """Test update profile bad field with fake access token

        Test:
            PATCH: /api/profile/<uuid>

        Expected result:
            400, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.patch("/api/profile/"+str(profile.uuid), headers=headers, json=dict(
            avatar="test"
        ))
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="test").first()

        assert response.status_code == 400
        assert res['status'] == False

    ### PROFILE PREFERENCES ###

    def test_profile_preferences_defined_no_jwt(self, test_client):
        """Test set profile preferences defined without access token

        Test:
            PUT: /api/profile/preferences_defined

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.put("/api/profile/preferences_defined")
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="test").first()

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
        assert profile.preferences_defined == False

    def test_profile_preferences_defined_fake_jwt(self, test_client, headers_fake):
        """Test set profile preferences defined with fake access token

        Test:
            PUT: /api/profile/preferences_defined

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.put(
            "/api/profile/preferences_defined", headers=headers_fake)
        res = json.loads(response.data)
        profile = ProfileModel.query.filter_by(profilename="test").first()

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_preferences_defined_bad_jwt(self, test_client, headers_bad):
        """Test profile set preferences defined with bad access token

        Test:
            PUT: /api/profile/preferences_defined

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.put(
            "/api/profile/preferences_defined", headers=headers_bad)

        assert response.status_code == 422

    ### SEARCH PROFILE ###

    def test_profile_search_no_jwt(self, test_client):
        """Test profile search without access token

        Test:
            GET: /api/profile/search/<profilename>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.get("/api/profile/search/"+profile.profilename)
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_search_bad_name(self, test_client, headers):
        """Test profile search bad name with access token

        Test:
            GET: /api/profile/search/<profilename>

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the access token
        """
        response = test_client.get(
            "/api/profile/search/"+str(uuid.uuid4()), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_profile_search(self, test_client, headers):
        """Test profile search with access token

        Test:
            GET: /api/profile/search/<profilename>

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.get(
            "/api/profile/search/"+profile.profilename, headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_profile_search_bad_jwt(self, test_client, headers_bad):
        """Test profile search with bad access token

        Test:
            GET: /api/profile/search/<profilename>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.get(
            "/api/profile/search/"+profile.profilename, headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_search_fake_jwt(self, test_client, headers_fake):
        """Test profile search with fake access token

        Test:
            GET: /api/profile/search/<profilename>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        profile = ProfileModel.query.filter_by(profilename="test").first()
        response = test_client.get(
            "/api/profile/search/"+profile.profilename, headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### PROFILE GENRE ###

    def test_profile_genre(self, test_client, headers):
        """Test get profile genres with access token

        Test:
            GET: /api/profile/genre

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.get("/api/profile/genre", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_profile_genre_bad_jwt(self, test_client, headers_bad):
        """Test profile genre with bad access token

        Test:
            GET: /api/profile/genre

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.get("/api/profile/genre", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_genre_fake_jwt(self, test_client, headers_fake):
        """Test get profile genre with fake access token

        Test:
            GET: /api/profile/genre

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.get("/api/profile/genre", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_genre_not_jwt(self, test_client):
        """Test get profile genre without access token

        Test:
            GET: /api/profile/genre

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/profile/genre")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### PROFILE GENRE ID - UPDATE ###

    def test_profile_genre_id(self, test_client, headers, genre_test1):
        """Test update profile genre by id with access token

        Test:
            PUT: /api/profile/genre/<genre_id>

        Expected result:
            201, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """

        response = test_client.put(
            "/api/profile/genre/"+str(genre_test1.genre_id), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_profile_genre_id_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test update profile genre by id  with fake access token

        Test:
            PUT: /api/profile/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.put(
            "/api/profile/genre/"+str(genre_test1.genre_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_genre_id_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test get profile genre id with bad access token

        Test:
            PUT: /api/profile/genre/<genre_id>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.put(
            "/api/profile/genre/"+str(genre_test1.genre_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_genre_id_no_jwt(self, test_client, genre_test1):
        """Test update profile genre by id without access token

        Test:
            PUT: /api/profile/genre/<genre_id>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.put(
            "/api/profile/genre/"+str(genre_test1.genre_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_genre_id_bad_id(self, test_client, headers):
        """Test profile genre by bad id with access token

        Test:
            PUT: /api/profile/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.put(
            "/api/profile/genre/"+str(9999999), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ###  PROFILE GENRE ID - DELETE ###

    def test_profile_genre_delete(self, test_client, headers, genre_test1):
        """Test delete profile genre by id with access token

        Test:
            DELETE: /api/profile/genre/<genre_id>

        Expected result:
            201, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.delete(
            "/api/profile/genre/"+str(genre_test1.genre_id), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_profile_genre_delete_id_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test delete profile genre by id with fake access token

        Test:
            DELETE: /api/profile/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.delete(
            "/api/profile/genre/"+str(genre_test1.genre_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_genre_delete_id_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test profile genre id delete with bad access token

        Test:
            DELETE: /api/profile/genre/<genre_id>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.delete(
            "/api/profile/genre/"+str(genre_test1.genre_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_genre_delete_id_no_jwt(self, test_client, genre_test1):
        """Test delete profile genre by id without access token

        Test:
            DELETE: /api/profile/genre/<genre_id>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        genre = GenreModel.query.filter_by(name="genre test").first()
        response = test_client.delete(
            "/api/profile/genre/"+str(genre_test1.genre_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_profile_genre_delete_id_bad_id(self, test_client, headers):
        """Test delete profile genre by bad id with access token

        Test:
            DELETE: /api/profile/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the access token
        """
        response = test_client.delete(
            "/api/profile/genre/"+str(9999999), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### EXPORT PROFILE DATA ###

    def test_profile_export_data(self, test_client, headers):
        """Test profile export data with access token

        Test:
            GET: /api/profile/export

        Expected result:
            200, {"status" : True, "profile" : ProfileObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """

        response = test_client.get("/api/profile/export", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['profile']['profilename'] == "profile"

    def test_profile_export_data_fake_jwt(self, test_client, headers_fake):
        """Test profile export data with fake access token

        Test:
            GET: /api/profile/export

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.get("/api/profile/export", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_profile_export_data_bad_jwt(self, test_client, headers_bad):
        """Test profile export data with bad access token

        Test:
            GET: /api/profile/export

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.get("/api/profile/export", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_profile_export_data_no_jwt(self, test_client):
        """Test  profile export resource without access token

        Test:
            GET: /api/profile/export

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/profile/export")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
