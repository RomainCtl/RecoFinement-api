import pytest
import json
from src.model import UserModel, GenreModel,ContentType
import uuid
from src import db

class TestUser:
    ### GET USER RESOURCE ###

    def test_user_resource(self, test_client, headers):
        """ Test user get resource

        Test:
            GET: /api/user/<uuid>

        Expected result:
            200, {"user": UserObject, "status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.get("/api/user/"+str(user.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res["user"]["email"] == user.email
    
    def test_user_resource_bad_jwt(self, test_client,headers_bad):
        """Test user get resource with bad access token

        Test:
            GET: /api/user/<uuid>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.get("/api/user/"+str(user.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_user_resource_fake_jwt(self, test_client,headers_fake):
        """Test get user resource with fake access token

        Test:
            GET: /api/user/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.get("/api/user/"+str(user.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_user_resource_no_jwt(self, test_client):
        """Test user get resource without access token

        Test:
            GET: /api/user/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.get("/api/user/"+str(user.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header" 

    def test_user_resource_bad_uuid(self, test_client, headers):
        """Test get user resource with bad uuid

        Test:
            GET: /api/user/<uuid>

        Expected result:
            404, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.get("/api/user/"+str(uuid.uuid4()), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### DELETE USER ###

    def test_delete_user_bad_jwt(self, test_client,headers_bad):
        """Test delete user with bad access token

        Test:
            DELETE: /api/user/<uuid>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.delete("/api/user/"+str(user.uuid), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_delete_user_fake_jwt(self, test_client, headers_fake):
        """Test delete user resource with fake access token

        Test:
            DELETE: /api/user/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.delete("/api/user/"+str(user.uuid), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_delete_user_no_jwt(self, test_client):
        """Test delete user resource without access token

        Test:
            DELETE: /api/user/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.delete("/api/user/"+str(user.uuid))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header" 

    def test_delete_user_bad_uuid(self, test_client, headers, user_test2):
        """Test delete user resource with bad uuid

        Test:
            DELETE: /api/user/<uuid>

        Expected result:
            403, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.delete("/api/user/"+str(user_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False
    
    def test_delete_user_other_user(self, test_client, headers, user_test2):
        """Test delete other user resource with access token

        Test:
            DELETE: /api/user/<uuid>

        Expected result:
            403, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the access token
        """
        response = test_client.delete("/api/user/"+str(user_test2.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False

    def test_delete_user(self, test_client, headers):
        """ Test user delete resource

        Test:
            DELETE: /api/user/<uuid>

        Expected result:
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.delete("/api/user/"+str(user.uuid), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    ### UPDATE USER ###

    def test_update_user(self, test_client, headers):
        """ Test user update resource

        Test:
            PATCH: /api/user/<uuid>

        Expected result:
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.patch("/api/user/"+str(user.uuid), headers=headers, json=dict(
            email = "test@test.bzh"
        ))
        res = json.loads(response.data)
        user =  UserModel.query.filter_by(username = "test").first()

        assert response.status_code == 201
        assert res['status'] == True
        assert user.email == "test@test.bzh"

    def test_update_user_bad_jwt(self, test_client,headers_bad):
        """Test user update with bad access token

        Test:
            PATCH: /api/user/<uuid>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.patch("/api/user/"+str(user.uuid), headers=headers_bad, json=dict(
            email = "test@test.com"
        ))
        res = json.loads(response.data)

        assert response.status_code == 422
        assert user.email == "test@test.bzh"

    def test_update_user_fake_jwt(self, test_client, headers_fake):
        """Test update user resource with fake access token

        Test:
            PATCH: /api/user/<uuid>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.patch("/api/user/"+str(user.uuid), headers=headers_fake, json=dict(
            email = "test@test.com"
        ))
        res = json.loads(response.data)
        user =  UserModel.query.filter_by(username = "test").first()

        assert response.status_code == 404
        assert res['status'] == False
        assert user.email == "test@test.bzh"
    
    def test_update_user_no_jwt(self, test_client):
        """Test update user resource without access token

        Test:
            PATCH: /api/user/<uuid>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.patch("/api/user/"+str(user.uuid), json=dict(
            email = "test@test.com"
        ))
        res = json.loads(response.data)
        user =  UserModel.query.filter_by(username = "test").first()

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
        assert user.email == "test@test.bzh"

    def test_update_user_bad_uuid(self, test_client, headers, user_test2):
        """Test update user resource with bad uuid

        Test:
            PATCH: /api/user/<uuid>

        Expected result:
            403, {"status" : False }

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.patch("/api/user/"+str(user_test2.uuid), headers=headers, json=dict(
            email = "test@test.com"
        ))
        res = json.loads(response.data)

        assert response.status_code == 403
        assert res['status'] == False

    def test_update_user_bad_field(self, test_client, headers):
        """Test update user bad field with fake access token

        Test:
            PATCH: /api/user/<uuid>

        Expected result:
            400, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        user =  UserModel.query.filter_by(username = "test").first()
        response = test_client.patch("/api/user/"+str(user.uuid), headers=headers, json=dict(
            avatar = "test@test.com"
        ))
        res = json.loads(response.data)
        user =  UserModel.query.filter_by(username = "test").first()

        assert response.status_code == 400
        assert res['status'] == False

    

    ### USER PREFERENCES ###

    def test_user_preferences_defined_no_jwt(self, test_client):
        """Test set user preferences defined without access token

        Test:
            PUT: /api/user/preferences_defined

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.put("/api/user/preferences_defined")
        res = json.loads(response.data)
        user =  UserModel.query.filter_by(username = "test").first()

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
        assert user.preferences_defined == False
    
    def test_user_preferences_defined_fake_jwt(self, test_client, headers_fake):
        """Test set user preferences defined with fake access token

        Test:
            PUT: /api/user/preferences_defined

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.put("/api/user/preferences_defined", headers=headers_fake)
        res = json.loads(response.data)
        user =  UserModel.query.filter_by(username = "test").first()

        assert response.status_code == 404
        assert res['status'] == False

    def test_user_preferences_defined_bad_jwt(self, test_client,headers_bad):
        """Test user set preferences defined with bad access token

        Test:
            PUT: /api/user/preferences_defined

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.put("/api/user/preferences_defined", headers=headers_bad)

        assert response.status_code == 422
    
    ### SEARCH USER ###

    def test_user_search_no_jwt(self, test_client):
        """Test user search without access token

        Test:
            GET: /api/user/search/<username>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        user = UserModel.query.filter_by(username="test").first()
        response = test_client.get("/api/user/search/"+user.username)
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_user_search_bad_name(self, test_client, headers):
        """Test user search bad name with access token

        Test:
            GET: /api/user/search/<username>

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the access token
        """
        response = test_client.get("/api/user/search/"+str(uuid.uuid4()), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_user_search(self, test_client, headers):
        """Test user search with access token

        Test:
            GET: /api/user/search/<username>

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        user = UserModel.query.filter_by(username="test").first()
        response = test_client.get("/api/user/search/"+user.username, headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
    
    def test_user_search_bad_jwt(self, test_client, headers_bad):
        """Test user search with bad access token

        Test:
            GET: /api/user/search/<username>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        user = UserModel.query.filter_by(username="test").first()
        response = test_client.get("/api/user/search/"+user.username, headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_user_search_fake_jwt(self, test_client, headers_fake):
        """Test user search with fake access token

        Test:
            GET: /api/user/search/<username>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): HTTP headers, to get the fake access token
        """
        user = UserModel.query.filter_by(username="test").first()
        response = test_client.get("/api/user/search/"+user.username, headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### USER GENRE ###
    
    def test_user_genre(self, test_client, headers):
        """Test get user genres with access token

        Test:
            GET: /api/user/genre

        Expected result:
            200, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.get("/api/user/genre", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_user_genre_bad_jwt(self, test_client, headers_bad):
        """Test user genre with bad access token

        Test:
            GET: /api/user/genre

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.get("/api/user/genre", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_user_genre_fake_jwt(self, test_client, headers_fake):
        """Test get user genre with fake access token

        Test:
            GET: /api/user/genre

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.get("/api/user/genre", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_user_genre_not_jwt(self, test_client):
        """Test get user genre without access token

        Test:
            GET: /api/user/genre

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/user/genre")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### USER GENRE ID - UPDATE ###

    def test_user_genre_id(self, test_client, headers, genre_test1):
        """Test update user genre by id with access token

        Test:
            PUT: /api/user/genre/<genre_id>

        Expected result:
            201, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        
        response = test_client.put("/api/user/genre/"+str(genre_test1.genre_id), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_user_genre_id_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test update user genre by id  with fake access token

        Test:
            PUT: /api/user/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.put("/api/user/genre/"+str(genre_test1.genre_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_user_genre_id_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test get user genre id with bad access token

        Test:
            PUT: /api/user/genre/<genre_id>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.put("/api/user/genre/"+str(genre_test1.genre_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_user_genre_id_no_jwt(self, test_client, genre_test1):
        """Test update user genre by id without access token

        Test:
            PUT: /api/user/genre/<genre_id>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.put("/api/user/genre/"+str(genre_test1.genre_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_user_genre_id_bad_id(self, test_client, headers):
        """Test user genre by bad id with access token

        Test:
            PUT: /api/user/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.put("/api/user/genre/"+str(9999999), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ###  USER GENRE ID - DELETE ###

    def test_user_genre_delete(self, test_client, headers, genre_test1):
        """Test delete user genre by id with access token

        Test:
            DELETE: /api/user/genre/<genre_id>

        Expected result:
            201, {"status" : True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        response = test_client.delete("/api/user/genre/"+str(genre_test1.genre_id), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True
    
    def test_user_genre_delete_id_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test delete user genre by id with fake access token

        Test:
            DELETE: /api/user/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.delete("/api/user/genre/"+str(genre_test1.genre_id), headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_user_genre_delete_id_bad_jwt(self, test_client, headers_bad,genre_test1):
        """Test user genre id delete with bad access token

        Test:
            DELETE: /api/user/genre/<genre_id>

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.delete("/api/user/genre/"+str(genre_test1.genre_id), headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_user_genre_delete_id_no_jwt(self, test_client,genre_test1):
        """Test delete user genre by id without access token

        Test:
            DELETE: /api/user/genre/<genre_id>

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        genre = GenreModel.query.filter_by(name="genre test").first()
        response = test_client.delete("/api/user/genre/"+str(genre_test1.genre_id))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_user_genre_delete_id_bad_id(self, test_client, headers):
        """Test delete user genre by bad id with access token

        Test:
            DELETE: /api/user/genre/<genre_id>

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the access token
        """
        response = test_client.delete("/api/user/genre/"+str(9999999), headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### EXPORT USER DATA ###

    def test_user_export_data(self, test_client, headers):
        """Test user export data with access token

        Test:
            GET: /api/user/export

        Expected result:
            200, {"status" : True, "user" : UserObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """

        response = test_client.get("/api/user/export", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['user']['email'] == "test@test.bzh"

    def test_user_export_data_fake_jwt(self, test_client, headers_fake):
        """Test user export data with fake access token

        Test:
            GET: /api/user/export

        Expected result:
            404, {"status" : False}

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the fake access token
        """
        response = test_client.get("/api/user/export", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_user_export_data_bad_jwt(self, test_client, headers_bad):
        """Test user export data with bad access token

        Test:
            GET: /api/user/export

        Expected result:
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): HTTP headers, to get the bad access token
        """
        response = test_client.get("/api/user/export", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_user_export_data_no_jwt(self, test_client):
        """Test  user export resource without access token

        Test:
            GET: /api/user/export

        Expected result:
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/user/export")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
