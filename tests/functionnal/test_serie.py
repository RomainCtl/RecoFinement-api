import pytest
import json
from src.model import SerieModel, MetaUserSerieModel
from src import db


class TestSerie:

    ### SERIE RESOURCE ###

    def test_serie_recommended(self, test_client, headers):
        """Test serie recommended

        Test:
            GET: /api/serie

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """

        if not (SerieModel.query.filter_by(serie_id=999999).first()):
            new_serie = SerieModel(
                serie_id=999999,
                title="test serie",
                rating=5.0,
                actors="authors serie",
                start_year="2019",
                end_year="2020",
                directors="director serie",
                writers="writer serie",
                imdbid="99999999",
                rating_count=1000,
                plot_outline="plot_outline serie",
                cover="cover"
            )
            db.session.add(new_serie)
            db.session.flush()
            db.session.commit()
        response = test_client.get("/api/serie", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_serie_recommended_one_page(self, test_client, headers):
        """Test serie get recommended serie page 1

        Test:
            GET: /api/serie?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/serie?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_serie_recommended_big_page(self, test_client, headers):
        """Test serie get recommended serie page 9999999

        Test:
            GET: /api/serie?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/serie?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_recommended_zero_page(self, test_client, headers):
        """Test serie get recommended serie page 0

        Test:
            GET: /api/serie?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/serie?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_recommended_negative_page(self, test_client, headers):
        """Test serie get recommended serie page -1

        Test:
            GET: /api/serie?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/serie?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_recommended_bad_jwt(self, test_client, headers_bad):
        """Test serie get recommended serie with bad JWT token 

        Test:
            GET: /api/serie

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            header_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/serie", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_recommended_fake_jwt(self, test_client, headers_fake):
        """Test serie get recommended serie with fake JWT token 

        Test:
            GET: /api/serie

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/serie", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_recommended_no_jwt(self, test_client):
        """Test serie get recommended serie without JWT token 

        Test:
            GET: /api/serie

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/serie")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### SERIE SEARCH ###

    def test_serie_search(self, test_client, headers):
        """Test serie search

        Test:
            GET: /api/serie/search/test serie

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_search_one_page(self, test_client, headers):
        """Test serie search get page 1

        Test:
            GET: /api/serie/search/test serie?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_serie_search_zero_page(self, test_client, headers):
        """Test serie search get page 0

        Test:
            GET: /api/serie/search/test serie?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_search_big_page(self, test_client, headers):
        """Test serie search get page 9999999

        Test:
            GET: /api/serie/search/test serie?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_search_negative_page(self, test_client, headers):
        """Test serie search get page -1

        Test:
            GET: /api/serie/search/test serie?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_search_bad_jwt(self, test_client, headers_bad):
        """Test serie search with bad JWT token 

        Test:
            GET: /api/serie/search/test serie

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_search_fake_jwt(self, test_client, headers_fake):
        """Test serie search with fake JWT token 

        Test:
            GET: /api/serie/search/test serie

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get(
            "/api/serie/search/test%20serie", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_search_no_jwt(self, test_client):
        """Test serie search without JWT token

        Test:
            GET: /api/serie/search/test serie

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/serie/search/test%20serie")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### SERIE GENRE ###

    def test_serie_genre(self, test_client, headers):
        """Test serie genre

        Test:
            GET: /api/serie/genres

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/serie/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_genre_no_jwt(self, test_client):
        """Test serie genre whithout JWT token

        Test:
            GET: /api/serie/genres

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/serie/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_serie_genre_bad_jwt(self, test_client, headers_bad):
        """Test serie genre with bad JWT token 

        Test:
            GET: /api/serie/genres

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/serie/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_genre_fake_jwt(self, test_client, headers_fake):
        """Test serie genre with fake JWT token 

        Test:
            GET: /api/serie/genres

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/serie/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### SERIE USER META ###

    def test_serie_user_meta(self, test_client, headers):
        """Test serie user meta

        Test:
            GET: /api/book/<serie_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(serie.serie_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_user_meta_bad_serie_id(self, test_client, headers):
        """Test serie user meta with bad serie_id

        Test:
            GET: /api/serie/<bad_serie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test serie user meta with bad JWT token 

        Test:
            GET: /api/serie/<serie_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test serie user meta with fake JWT token 

        Test:
            GET: /api/serie/<serie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_no_jwt(self, test_client):
        """Test serie user mate without JWT token

        Test:
            GET: /api/serie/<serie_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get("/api/serie/"+str(serie.serie_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### SERIE USER META UPDATE ###

    def test_serie_user_meta_update(self, test_client, headers, user_test1):
        """Test serie user meta update

        Test:
            PATCH: /api/serie/<serie_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers, json=dict(
            rating=5,
            num_watched_episodes=5,

        ))
        res = json.loads(response.data)
        meta = MetaUserSerieModel.query.filter_by(
            user_id=user_test1.user_id, serie_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.rating == 5
        assert meta.num_watched_episodes == 5

    def test_serie_user_meta_update_bad_serie_id(self, test_client, headers):
        """Test serie user meta update with bad serie_id

        Test:
            PATCH: /api/serie/<bad_serie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.patch("/api/serie/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            num_watched_episodes=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test serie user meta update with bad JWT token 

        Test:
            PATCH: /api/serie/<serie_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            num_watched_episodes=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test serie user meta update with fake JWT token 

        Test:
            PATCH: /api/serie/<serie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            num_watched_episodes=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_update_no_jwt(self, test_client):
        """Test serie user meta update without JWT token 

        Test:
            PATCH: /api/serie/<serie_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", json=dict(
            rating=5,
            num_watched_episodes=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_serie_user_meta_update_bad_field(self, test_client, headers):
        """Test serie user meta update with bad field

        Test:
            PATCH: /api/serie/<serie_id>/meta

        Expected result: 
            400, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers, json=dict(
            bad_field=5,
        ))
        res = json.loads(response.data)
        
        assert response.status_code == 400
        assert res['status'] == False


    ### SERIE BAD RECOMMENDATION ###

    def test_serie_bad_recommendation(self, test_client, headers):
        """Test serie bad recommendation

        Test:
            GET: /api/serie/<int:serie_id>/bad_recommendation

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.serie_id)+"/bad_recommendation", headers=headers, json=dict(
            start_year=["2010"]
        ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_serie_bad_recommendation_bad_serie_id(self, test_client, headers):
        """Test serie bad recommendation with bad serie ID

        Test:
            GET: /api/serie/<int:serie_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.post(
            "/api/serie/"+str(999999999)+"/bad_recommendation", headers=headers, json=dict(
            start_year=["2010"]
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_bad_recommendation_bad_jwt(self, test_client, headers_bad):
        """Test serie bad recommendation with bad JWT token

        Test:
            GET: /api/serie/<int:serie_id>/bad_recommendation

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.serie_id)+"/bad_recommendation", headers=headers_bad, json=dict(
            start_year=["2010"]
        ))
        #res = json.loads(response.data)

        assert response.status_code == 422
    
    def test_serie_bad_recommendation_fake_jwt(self, test_client, headers_fake):
        """Test serie bad recommendation with fake JWT token

        Test:
            GET: /api/serie/<int:serie_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.serie_id)+"/bad_recommendation", headers=headers_fake, json=dict(
            start_year=["2010"]
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_bad_recommendation_no_jwt(self, test_client):
        """Test serie bad recommendation without JWT token

        Test:
            GET: /api/serie/<int:serie_id>/bad_recommendation

        Expected result: 
            401, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.serie_id)+"/bad_recommendation", json=dict(
            start_year=["2010"]
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_serie_bad_recommendation_bad_field(self, test_client, headers):
        """Test serie bad recommendation with bad field

        Test:
            GET: /api/serie/<int:serie_id>/bad_recommendation

        Expected result: 
            400, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.serie_id)+"/bad_recommendation", headers=headers, json=dict(
            bad_field=["2010"]
        ))
        res = json.loads(response.data)

        assert response.status_code == 400
        assert res['status'] == False
