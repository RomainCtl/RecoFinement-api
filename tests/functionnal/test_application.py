import pytest
import json
from src.model import ApplicationModel, ContentModel, MetaUserContentModel
from src import db


class TestApplication:

    ### APPLICATION RESOURCE ###

    def test_application_recommended(self, test_client, headers):
        """Test application recommended

        Test:
            GET: /api/application

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        if not (ApplicationModel.query.filter_by(content_id=999999).first()):
            content = ContentModel(
                content_id=999999, rating=5.0, rating_count=4)
            db.session.add(content)
            db.session.flush()
            new_app = ApplicationModel(
                name="test app",
                size="145mb",
                installs="110k",
                type="chat",
                price="free",
                content_rating="top",
                last_updated="11/10/2020",
                current_version="1.4",
                android_version="10.1",
                cover="cover",
                content=content
            )
            db.session.add(new_app)
            db.session.flush()
            db.session.commit()
        response = test_client.get("/api/application", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_application_recommended_one_page(self, test_client, headers):
        """Test application get recommended application page 1

        Test:
            GET: /api/application?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/application?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_application_recommended_big_page(self, test_client, headers):
        """Test application get recommended application page 9999999

        Test:
            GET: /api/application?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/application?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_recommended_zero_page(self, test_client, headers):
        """Test application get recommended application page 0

        Test:
            GET: /api/application?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/application?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_recommended_negative_page(self, test_client, headers):
        """Test application get recommended application page -1

        Test:
            GET: /api/application?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/application?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_recommended_bad_jwt(self, test_client, headers_bad):
        """Test application get recommended application with bad JWT token 

        Test:
            GET: /api/application

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            header_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/application", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_recommended_fake_jwt(self, test_client, headers_fake):
        """Test application get recommended application with fake JWT token 

        Test:
            GET: /api/application

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/application", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_recommended_no_jwt(self, test_client):
        """Test application get recommended application without JWT token 

        Test:
            GET: /api/application

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/application")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### APPLICATION SEARCH ###

    def test_application_search(self, test_client, headers):
        """Test application search

        Test:
            GET: /api/application/search/test app

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/application/search/test%20app", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_application_search_one_page(self, test_client, headers):
        """Test application search get page 1

        Test:
            GET: /api/application/search/test app?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/application/search/test%20app?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_application_search_zero_page(self, test_client, headers):
        """Test application search get page 0

        Test:
            GET: /api/application/search/test app?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/application/search/test%20app?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_search_big_page(self, test_client, headers):
        """Test application search get page 9999999

        Test:
            GET: /api/application/search/test app?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/application/search/test%20app?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_search_negative_page(self, test_client, headers):
        """Test application search get page -1

        Test:
            GET: /api/application/search/test app?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/application/search/test%20app?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_search_bad_jwt(self, test_client, headers_bad):
        """Test application search with bad JWT token 

        Test:
            GET: /api/application/search/test app

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get(
            "/api/application/search/test%20app", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_search_fake_jwt(self, test_client, headers_fake):
        """Test application search with fake JWT token 

        Test:
            GET: /api/application/search/test app

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get(
            "/api/application/search/test%20app", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_search_no_jwt(self, test_client):
        """Test application search without JWT token

        Test:
            GET: /api/application/search/test app

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/application/search/test%20app")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### APPLICATION GENRE ###

    def test_application_genre(self, test_client, headers):
        """Test application genre

        Test:
            GET: /api/application/genres

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/application/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_application_genre_no_jwt(self, test_client):
        """Test application genre whithout JWT token

        Test:
            GET: /api/application/genres

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/application/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_application_genre_bad_jwt(self, test_client, headers_bad):
        """Test application genre with bad JWT token 

        Test:
            GET: /api/application/genres

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get(
            "/api/application/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_genre_fake_jwt(self, test_client, headers_fake):
        """Test application genre with fake JWT token 

        Test:
            GET: /api/application/genres

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get(
            "/api/application/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### APPLICATION USER META ###

    def test_application_user_meta(self, test_client, headers):
        """Test application user meta

        Test:
            GET: /api/book/<content_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/application/"+str(app.content_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_application_user_meta_bad_content_id(self, test_client, headers):
        """Test application user meta with bad content_id

        Test:
            GET: /api/application/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/application/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test application user meta with bad JWT token 

        Test:
            GET: /api/application/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/application/"+str(app.content_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test application user meta with fake JWT token 

        Test:
            GET: /api/application/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/application/"+str(app.content_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_no_jwt(self, test_client):
        """Test application user mate without JWT token

        Test:
            GET: /api/application/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/application/"+str(app.content_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### APPLICATION USER META UPDATE ###

    def test_application_user_meta_update(self, test_client, headers, user_test1):
        """Test application user meta update

        Test:
            PATCH: /api/application/<content_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.content_id)+"/meta", headers=headers, json=dict(
            rating=5,
        ))
        res = json.loads(response.data)
        meta = MetaUserContentModel.query.filter_by(
            user_id=user_test1.user_id, content_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.rating == 5

    def test_application_user_meta_update_bad_content_id(self, test_client, headers):
        """Test application user meta update with bad content_id

        Test:
            PATCH: /api/application/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/application/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test application user meta update with bad JWT token 

        Test:
            PATCH: /api/application/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.content_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test application user meta update with fake JWT token 

        Test:
            PATCH: /api/application/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.content_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_update_no_jwt(self, test_client):
        """Test application user meta update without JWT token 

        Test:
            PATCH: /api/application/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        app = ApplicationModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.content_id)+"/meta", json=dict(
            rating=5,
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### APPLICATION BAD RECOMMENDATION ###

    def test_application_bad_recommendation(self, test_client, headers):
        """Test application bad recommendation

        Test:
            GET: /api/application/<int:application_id>/bad_recommendation

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        application = ApplicationModel.query.filter_by(
            content_id=999999).first()
        response = test_client.post(
            "/api/application/"+str(application.content_id)+"/bad_recommendation", headers=headers, json=dict(
                categorie=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_application_bad_recommendation_bad_application_id(self, test_client, headers):
        """Test application bad recommendation with bad application ID

        Test:
            GET: /api/application/<int:application_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.post(
            "/api/application/"+str(999999999)+"/bad_recommendation", headers=headers, json=dict(
                categorie=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_bad_recommendation_bad_jwt(self, test_client, headers_bad):
        """Test application bad recommendation with bad JWT token

        Test:
            GET: /api/application/<int:application_id>/bad_recommendation

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        application = ApplicationModel.query.filter_by(
            content_id=999999).first()
        response = test_client.post(
            "/api/application/"+str(application.content_id)+"/bad_recommendation", headers=headers_bad, json=dict(
                categorie=["2010"]
            ))
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_bad_recommendation_fake_jwt(self, test_client, headers_fake):
        """Test application bad recommendation with fake JWT token

        Test:
            GET: /api/application/<int:application_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        application = ApplicationModel.query.filter_by(
            content_id=999999).first()
        response = test_client.post(
            "/api/application/"+str(application.content_id)+"/bad_recommendation", headers=headers_fake, json=dict(
                categorie=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_bad_recommendation_no_jwt(self, test_client):
        """Test application bad recommendation without JWT token

        Test:
            GET: /api/application/<int:application_id>/bad_recommendation

        Expected result: 
            401, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        application = ApplicationModel.query.filter_by(
            content_id=999999).first()
        response = test_client.post(
            "/api/application/"+str(application.content_id)+"/bad_recommendation", json=dict(
                categorie=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### APPLICATION ADD CONTENT ###
    def test_application_add_content(self, test_client, headers, genre_test1):
        """Test application add additional content
        Test:
            POST: /api/application/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/application", headers=headers, json=dict(
                name="name",
                size="size",
                installs="installs",
                type="type",
                price="price",
                content_rating="content_rating",
                last_updated="last_updated",
                current_version="current_version",
                android_version="android_version",
                cover="cover",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True
