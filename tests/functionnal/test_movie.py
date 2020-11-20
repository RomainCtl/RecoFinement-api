import pytest
import json
from src.model import MovieModel, MetaUserMovieModel
from src import db

class TestMovie:

    ### MOVIE RESOURCE ###

    def test_movie_recommended(self, test_client, headers):
        """Test movie recommended

        Test:
            GET: /api/movie

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        if not (MovieModel.query.filter_by(movie_id=999999).first()):
            new_movie = MovieModel(
                movie_id = 999999,
                title="test movie",
                language="FR",
                rating=5.0,
                actors="authors movie",
                year= "2020",
                producers="producers movie",
                director = "director movie",
                writer = "writer movie",
                imdbid = "99999999",
                tmdbid =  "99999999",
                rating_count = 1000,
                plot_outline = "plot_outline movie",
                cover = "cover"
            )
            db.session.add(new_movie)
            db.session.flush()
            db.session.commit()
        response = test_client.get("/api/movie", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_movie_recommended_one_page(self, test_client, headers):
        """Test movie get recommended movie page 1

        Test:
            GET: /api/movie?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []
    
    def test_movie_recommended_big_page(self, test_client, headers):
        """Test movie get recommended movie page 9999999

        Test:
            GET: /api/movie?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_movie_recommended_zero_page(self, test_client, headers):
        """Test movie get recommended movie page 0

        Test:
            GET: /api/movie?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_movie_recommended_negative_page(self, test_client, headers):
        """Test movie get recommended movie page -1

        Test:
            GET: /api/movie?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_movie_recommended_bad_jwt(self, test_client, headers_bad):
        """Test movie get recommended movie with bad JWT token 

        Test:
            GET: /api/movie

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            header_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/movie", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_movie_recommended_fake_jwt(self, test_client, headers_fake):
        """Test movie get recommended movie with fake JWT token 

        Test:
            GET: /api/movie

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/movie", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_movie_recommended_no_jwt(self, test_client):
        """Test movie get recommended movie without JWT token 

        Test:
            GET: /api/movie

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/movie")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### MOVIE SEARCH ###

    def test_movie_search(self, test_client, headers):
        """Test movie search

        Test:
            GET: /api/movie/search/test movie

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie/search/test%20movie", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_movie_search_one_page(self, test_client, headers):
        """Test movie search get page 1

        Test:
            GET: /api/movie/search/test movie?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie/search/test%20movie?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_movie_search_zero_page(self, test_client, headers):
        """Test movie search get page 0

        Test:
            GET: /api/movie/search/test movie?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie/search/test%20movie?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_movie_search_big_page(self, test_client, headers):
        """Test movie search get page 9999999

        Test:
            GET: /api/movie/search/test movie?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie/search/test%20movie?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_movie_search_negative_page(self, test_client, headers):
        """Test movie search get page -1

        Test:
            GET: /api/movie/search/test movie?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie/search/test%20movie?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_movie_search_bad_jwt(self, test_client, headers_bad):
        """Test movie search with bad JWT token 

        Test:
            GET: /api/movie/search/test movie

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/movie/search/test%20movie", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_movie_search_fake_jwt(self, test_client, headers_fake):
        """Test movie search with fake JWT token 

        Test:
            GET: /api/movie/search/test movie

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/movie/search/test%20movie", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_movie_search_no_jwt(self, test_client):
        """Test movie search without JWT token

        Test:
            GET: /api/movie/search/test movie

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/movie/search/test%20movie")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### MOVIE GENRE ###

    def test_movie_genre(self, test_client, headers):
        """Test movie genre

        Test:
            GET: /api/movie/genres

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/movie/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_movie_genre_no_jwt(self, test_client):
        """Test movie genre whithout JWT token

        Test:
            GET: /api/movie/genres

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/movie/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_movie_genre_bad_jwt(self, test_client, headers_bad):
        """Test movie genre with bad JWT token 

        Test:
            GET: /api/movie/genres

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/movie/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_movie_genre_fake_jwt(self, test_client, headers_fake):
        """Test movie genre with fake JWT token 

        Test:
            GET: /api/movie/genres

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/movie/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### MOVIE USER META ###

    def test_movie_user_meta(self, test_client, headers):
        """Test movie user meta

        Test:
            GET: /api/book/<movie_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.get("/api/movie/"+str(app.movie_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_movie_user_meta_bad_movie_id(self, test_client, headers):
        """Test movie user meta with bad movie_id

        Test:
            GET: /api/movie/<bad_movie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.get("/api/movie/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_movie_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test movie user meta with bad JWT token 

        Test:
            GET: /api/movie/<movie_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.get("/api/movie/"+str(app.movie_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_movie_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test movie user meta with fake JWT token 

        Test:
            GET: /api/movie/<movie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.get("/api/movie/"+str(app.movie_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_movie_user_meta_no_jwt(self, test_client):
        """Test movie user mate without JWT token

        Test:
            GET: /api/movie/<movie_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.get("/api/movie/"+str(app.movie_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### MOVIE USER META UPDATE ###
    
    def test_movie_user_meta_update(self, test_client, headers, user_test1):
        """Test movie user meta update

        Test:
            PATCH: /api/movie/<movie_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.patch("/api/movie/"+str(app.movie_id)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_watch_count = 10
        ))
        res = json.loads(response.data)
        meta = MetaUserMovieModel.query.filter_by(user_id=user_test1.user_id,movie_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.rating == 5
        assert meta.watch_count == 10

    def test_movie_user_meta_update_bad_movie_id(self, test_client, headers):
        """Test movie user meta update with bad movie_id

        Test:
            PATCH: /api/movie/<bad_movie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.patch("/api/movie/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_watch_count = 10
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_movie_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test movie user meta update with bad JWT token 

        Test:
            PATCH: /api/movie/<movie_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.patch("/api/movie/"+str(app.movie_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_watch_count = 10
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_movie_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test movie user meta update with fake JWT token 

        Test:
            PATCH: /api/movie/<movie_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.patch("/api/movie/"+str(app.movie_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_watch_count = 10
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_movie_user_meta_update_no_jwt(self, test_client):
        """Test movie user meta update without JWT token 

        Test:
            PATCH: /api/movie/<movie_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        app = MovieModel.query.filter_by(movie_id=999999).first()
        response = test_client.patch("/api/movie/"+str(app.movie_id)+"/meta", json=dict(
            rating=5,
            additional_watch_count = 10
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
