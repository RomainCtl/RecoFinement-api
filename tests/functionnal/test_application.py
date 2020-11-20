import pytest
import json
from src.model import ApplicationModel, MetaUserApplicationModel
from src import db

class TestApplication:

    ### APPLICATION RESOURCE ###

    def test_application_recommended(self, test_client, headers):
        if not (ApplicationModel.query.filter_by(app_id=999999).first()):
            new_app = ApplicationModel(
                app_id = 999999,
                name="test app",
                genre_id=1,
                rating=5.0,
                reviews=4,
                size= "145mb",
                installs="110k",
                type = "chat",
                price = "free",
                content_rating = "top",
                last_updated = "11/10/2020",
                current_version ="1.4",
                android_version = "10.1",
                cover = "cover"
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
        response = test_client.get("/api/application?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []
    
    def test_application_recommended_big_page(self, test_client, headers):
        response = test_client.get("/api/application?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_application_recommended_zero_page(self, test_client, headers):
        response = test_client.get("/api/application?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_recommended_negative_page(self, test_client, headers):
        response = test_client.get("/api/application?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_application_recommended_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/application", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_recommended_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/application", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_application_recommended_no_jwt(self, test_client):
        response = test_client.get("/api/application")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### APPLICATION SEARCH ###

    def test_application_search(self, test_client, headers):
        response = test_client.get("/api/application/search/test%20app", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_application_search_one_page(self, test_client, headers):
        response = test_client.get("/api/application/search/test%20app?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_application_search_zero_page(self, test_client, headers):
        response = test_client.get("/api/application/search/test%20app?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_application_search_big_page(self, test_client, headers):
        response = test_client.get("/api/application/search/test%20app?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_application_search_negative_page(self, test_client, headers):
        response = test_client.get("/api/application/search/test%20app?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_application_search_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/application/search/test%20app", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_search_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/application/search/test%20app", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_application_search_no_jwt(self, test_client):
        response = test_client.get("/api/application/search/test%20app")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### APPLICATION GENRE ###

    def test_application_genre(self, test_client, headers):
        response = test_client.get("/api/application/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_application_genre_no_jwt(self, test_client):
        response = test_client.get("/api/application/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_application_genre_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/application/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_genre_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/application/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### APPLICATION USER META ###

    def test_application_user_meta(self, test_client, headers):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.get("/api/application/"+str(app.app_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_application_user_meta_bad_app_id(self, test_client, headers):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.get("/api/application/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_bad_jwt(self, test_client, headers_bad):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.get("/api/application/"+str(app.app_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_user_meta_fake_jwt(self, test_client, headers_fake):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.get("/api/application/"+str(app.app_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_no_jwt(self, test_client):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.get("/api/application/"+str(app.app_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### APPLICATION USER META UPDATE ###
    
    def test_application_user_meta_update(self, test_client, headers, user_test1):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.app_id)+"/meta", headers=headers, json=dict(
            rating=5,
            review="review test",
            downloaded=True
        ))
        res = json.loads(response.data)
        meta = MetaUserApplicationModel.query.filter_by(user_id=user_test1.user_id,app_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.downloaded == True
        assert meta.rating == 5
        assert meta.review == "review test"

    def test_application_user_meta_update_bad_app_id(self, test_client, headers):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.patch("/api/application/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            review="review test",
            downloaded=True
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_update_bad_jwt(self, test_client, headers_bad):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.app_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            review="review test",
            downloaded=True
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_application_user_meta_update_fake_jwt(self, test_client, headers_fake):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.app_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            review="review test",
            downloaded=True
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_application_user_meta_update_no_jwt(self, test_client):
        app = ApplicationModel.query.filter_by(app_id=999999).first()
        response = test_client.patch("/api/application/"+str(app.app_id)+"/meta", json=dict(
            rating=5,
            review="review test",
            downloaded=True
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
