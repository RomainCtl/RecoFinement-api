import pytest
import json
from src.model import SerieModel, ContentModel, MetaUserContentModel, SerieAdditionalModel
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

        if not (SerieModel.query.filter_by(content_id=999999).first()):
            content = ContentModel(
                content_id=999999, rating=5.0, rating_count=1000)
            db.session.add(content)
            db.session.flush()
            new_serie = SerieModel(
                title="test serie",
                actors="authors serie",
                start_year="2019",
                end_year="2020",
                directors="director serie",
                writers="writer serie",
                imdbid="99999999",
                plot_outline="plot_outline serie",
                cover="cover",
                content=content,
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
            GET: /api/serie/<content_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(serie.content_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_user_meta_bad_content_id(self, test_client, headers):
        """Test serie user meta with bad content_id

        Test:
            GET: /api/serie/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test serie user meta with bad JWT token 

        Test:
            GET: /api/serie/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(serie.content_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test serie user meta with fake JWT token 

        Test:
            GET: /api/serie/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/serie/"+str(serie.content_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_no_jwt(self, test_client):
        """Test serie user mate without JWT token

        Test:
            GET: /api/serie/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.get("/api/serie/"+str(serie.content_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### SERIE USER META UPDATE ###

    def test_serie_user_meta_update(self, test_client, headers, user_test1):
        """Test serie user meta update

        Test:
            PATCH: /api/serie/<content_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.content_id)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=5,

        ))
        res = json.loads(response.data)
        meta = MetaUserContentModel.query.filter_by(
            user_id=user_test1.user_id, content_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.rating == 5
        assert meta.count == 5  # num_whatched_episode

    def test_serie_user_meta_update_bad_content_id(self, test_client, headers):
        """Test serie user meta update with bad content_id

        Test:
            PATCH: /api/serie/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.patch("/api/serie/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test serie user meta update with bad JWT token 

        Test:
            PATCH: /api/serie/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.content_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_count=5
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test serie user meta update with fake JWT token 

        Test:
            PATCH: /api/serie/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.content_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_count=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_update_no_jwt(self, test_client):
        """Test serie user meta update without JWT token 

        Test:
            PATCH: /api/serie/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.content_id)+"/meta", json=dict(
            rating=5,
            additional_count=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### SERIE BAD RECOMMENDATION ###

    def test_serie_bad_recommendation(self, test_client, headers):
        """Test serie bad recommendation

        Test:
            GET: /api/serie/<int:content_id>/bad_recommendation

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.content_id)+"/bad_recommendation", headers=headers, json=dict(
                start_year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_serie_bad_recommendation_bad_content_id(self, test_client, headers):
        """Test serie bad recommendation with bad serie ID

        Test:
            GET: /api/serie/<int:content_id>/bad_recommendation

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
            GET: /api/serie/<int:content_id>/bad_recommendation

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.content_id)+"/bad_recommendation", headers=headers_bad, json=dict(
                start_year=["2010"]
            ))
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_bad_recommendation_fake_jwt(self, test_client, headers_fake):
        """Test serie bad recommendation with fake JWT token

        Test:
            GET: /api/serie/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.content_id)+"/bad_recommendation", headers=headers_fake, json=dict(
                start_year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_bad_recommendation_no_jwt(self, test_client):
        """Test serie bad recommendation without JWT token

        Test:
            GET: /api/serie/<int:content_id>/bad_recommendation

        Expected result: 
            401, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        serie = SerieModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/serie/"+str(serie.content_id)+"/bad_recommendation", json=dict(
                start_year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### SERIE ADD CONTENT ###
    def test_serie_add_content(self, test_client, headers, genre_test1):
        """Test serie add additional content
        Test:
            POST: /api/serie/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/serie", headers=headers, json=dict(
                title="title",
                imdbid="imdbid",
                start_year=1900,
                end_year=1900,
                writers="writer1 | writer2",
                directors="director1 | director2",
                actors="actor1 | actor2",
                cover="cover",
                episodes=[dict(
                    title="title",
                    imdbid="imdbid",
                    year=1900,
                    season_number=1,
                    episode_number=1,
                    genres=[genre_test1.genre_id],
                )],
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_serie_add_minimal_content(self, test_client, headers, genre_test1):
        """Test serie add additional minimal content
        Test:
            POST: /api/serie/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/serie", headers=headers, json=dict(
                title="title2",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_serie_add_content_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test serie add additional minimal content with bad JWT token
        Test:
            POST: /api/serie/
        Expected result: 
            422
        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, to get the access token
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/serie", headers=headers_bad, json=dict(
                title="title2",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_add_content_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test serie add additional minimal content with fake JWT token
        Test:
            POST: /api/serie/
        Expected result: 
            404, {"status": False}
        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/serie", headers=headers_fake, json=dict(
                title="title2",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_add_content_no_jwt(self, test_client, genre_test1):
        """Test serie add additional minimal content without JWT token
        Test:
            POST: /api/serie/
        Expected result: 
            401, {"status": False}
        Args:
            test_client (app context): Flask application
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/serie", json=dict(
                title="title2",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
        
    ### SERIE GET ADDITIONAL CONTENT ###
    def test_serie_get_additional_content(self, test_client, headers):
        """Test serie get additional content
        Test:
            GET: /api/serie/additional/
        Expected result: 
            200, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/serie/additional", headers=headers)
        res = json.loads(response.data)
        
        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    ### SERIE VALIDATE CONTENT ###
    def test_serie_validate_additional_content(self, test_client, headers_admin):
        """Test serie validate additional content
        Test:
            PUT: /api/serie/<int:serie_id>
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieAdditionalModel.query.filter_by(title="title").first()
        response = test_client.put("/api/serie/additional/"+str(serie.serie_id), headers=headers_admin)

        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

        
    ### SERIE DECLINE CONTENT ###
    def test_serie_decline_additional_content(self, test_client, headers_admin):
        """Test serie validate decline content
        Test:
            DELETE: /api/serie/<int:serie_id>
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        serie = SerieAdditionalModel.query.filter_by(title="title2").first()
        response = test_client.delete("/api/serie/additional/"+str(serie.serie_id), headers=headers_admin)

        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True