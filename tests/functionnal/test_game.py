import pytest
import json
from src.model import GameModel, ContentModel, MetaUserContentModel, GameAdditionalModel
from src import db


class TestGame:

    ### GAME RESOURCE ###

    def test_game_recommended(self, test_client, headers):
        """Test game recommended

        Test:
            GET: /api/game

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        if not (GameModel.query.filter_by(content_id=999999).first()):
            content = ContentModel(
                content_id=999999, rating=5.0, rating_count=10)
            db.session.add(content)
            db.session.flush()
            new_game = GameModel(
                steamid=999999,
                name="test game",
                short_description="short desc game",
                header_image="header img",
                website="website",
                developers="dev",
                publishers="publishers",
                price="free",
                recommendations=150,
                release_date="11/10/2020",
                content=content
            )
            db.session.add(new_game)
            db.session.flush()
            db.session.commit()
        response = test_client.get("/api/game", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_game_recommended_one_page(self, test_client, headers):
        """Test game get recommended game page 1

        Test:
            GET: /api/game?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/game?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_game_recommended_big_page(self, test_client, headers):
        """Test game get recommended game page 9999999

        Test:
            GET: /api/game?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/game?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_recommended_zero_page(self, test_client, headers):
        """Test game get recommended game page 0

        Test:
            GET: /api/game?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/game?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_recommended_negative_page(self, test_client, headers):
        """Test game get recommended game page -1

        Test:
            GET: /api/game?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/game?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_recommended_bad_jwt(self, test_client, headers_bad):
        """Test game get recommended game with bad JWT token 

        Test:
            GET: /api/game

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            header_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/game", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_recommended_fake_jwt(self, test_client, headers_fake):
        """Test game get recommended game with fake JWT token 

        Test:
            GET: /api/game

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/game", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_recommended_no_jwt(self, test_client):
        """Test game get recommended game without JWT token 

        Test:
            GET: /api/game

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/game")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GAME SEARCH ###

    def test_game_search(self, test_client, headers):
        """Test game search

        Test:
            GET: /api/game/search/test game

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/game/search/test%20game", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_game_search_one_page(self, test_client, headers):
        """Test game search get page 1

        Test:
            GET: /api/game/search/test game?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/game/search/test%20game?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_game_search_zero_page(self, test_client, headers):
        """Test game search get page 0

        Test:
            GET: /api/game/search/test game?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/game/search/test%20game?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_search_big_page(self, test_client, headers):
        """Test game search get page 9999999

        Test:
            GET: /api/game/search/test game?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/game/search/test%20game?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_search_negative_page(self, test_client, headers):
        """Test game search get page -1

        Test:
            GET: /api/game/search/test game?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/game/search/test%20game?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_search_bad_jwt(self, test_client, headers_bad):
        """Test game search with bad JWT token 

        Test:
            GET: /api/game/search/test game

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get(
            "/api/game/search/test%20game", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_search_fake_jwt(self, test_client, headers_fake):
        """Test game search with fake JWT token 

        Test:
            GET: /api/game/search/test game

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get(
            "/api/game/search/test%20game", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_search_no_jwt(self, test_client):
        """Test game search without JWT token

        Test:
            GET: /api/game/search/test game

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/game/search/test%20game")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GAME GENRE ###

    def test_game_genre(self, test_client, headers):
        """Test game genre

        Test:
            GET: /api/game/genres

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/game/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_game_genre_no_jwt(self, test_client):
        """Test game genre whithout JWT token

        Test:
            GET: /api/game/genres

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/game/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_game_genre_bad_jwt(self, test_client, headers_bad):
        """Test game genre with bad JWT token 

        Test:
            GET: /api/game/genres

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/game/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_genre_fake_jwt(self, test_client, headers_fake):
        """Test game genre with fake JWT token 

        Test:
            GET: /api/game/genres

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/game/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### GAME USER META ###

    def test_game_user_meta(self, test_client, headers):
        """Test game user meta

        Test:
            GET: /api/game/<content_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/game/"+str(game.content_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_game_user_meta_bad_content_id(self, test_client, headers):
        """Test game user meta with bad content_id

        Test:
            GET: /api/game/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/game/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test game user meta with bad JWT token 

        Test:
            GET: /api/game/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/game/"+str(game.content_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test game user meta with fake JWT token 

        Test:
            GET: /api/game/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/game/"+str(game.content_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_no_jwt(self, test_client):
        """Test game user mate without JWT token

        Test:
            GET: /api/game/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.get("/api/game/"+str(game.content_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GAME USER META UPDATE ###

    def test_game_user_meta_update(self, test_client, headers, user_test1):
        """Test game user meta update

        Test:
            PATCH: /api/game/<content_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.content_id)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=24.0
        ))

        res = json.loads(response.data)
        meta = MetaUserContentModel.query.filter_by(
            user_id=user_test1.user_id, content_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.rating == 5
        assert meta.count == 24.0

    def test_game_user_meta_update_bad_content_id(self, test_client, headers):
        """Test game user meta update with bad content_id

        Test:
            PATCH: /api/game/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/game/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=24.0
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test game user meta update with bad JWT token 

        Test:
            PATCH: /api/game/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.content_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_count=24.0
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test game user meta update with fake JWT token 

        Test:
            PATCH: /api/game/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.content_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_count=24.0
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_update_no_jwt(self, test_client):
        """Test game user meta update without JWT token 

        Test:
            PATCH: /api/game/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.content_id)+"/meta", json=dict(
            rating=5,
            additional_count=24.0
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GAME BAD RECOMMENDATION ###

    def test_game_bad_recommendation(self, test_client, headers):
        """Test game bad recommendation

        Test:
            GET: /api/game/<int:content_id>/bad_recommendation

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/game/"+str(game.content_id)+"/bad_recommendation", headers=headers, json=dict(
                developers=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_game_bad_recommendation_bad_content_id(self, test_client, headers):
        """Test game bad recommendation with bad game ID

        Test:
            GET: /api/game/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.post(
            "/api/game/"+str(999999999)+"/bad_recommendation", headers=headers, json=dict(
                developers=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_bad_recommendation_bad_jwt(self, test_client, headers_bad):
        """Test game bad recommendation with bad JWT token

        Test:
            GET: /api/game/<int:content_id>/bad_recommendation

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/game/"+str(game.content_id)+"/bad_recommendation", headers=headers_bad, json=dict(
                developers=["2010"]
            ))
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_bad_recommendation_fake_jwt(self, test_client, headers_fake):
        """Test game bad recommendation with fake JWT token

        Test:
            GET: /api/game/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/game/"+str(game.content_id)+"/bad_recommendation", headers=headers_fake, json=dict(
                developers=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_bad_recommendation_no_jwt(self, test_client):
        """Test game bad recommendation without JWT token

        Test:
            GET: /api/game/<int:content_id>/bad_recommendation

        Expected result: 
            401, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        game = GameModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/game/"+str(game.content_id)+"/bad_recommendation", json=dict(
                developers=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GAME ADD CONTENT ###
    def test_game_add_content(self, test_client, headers, genre_test1):
        """Test game add additional content
        Test:
            POST: /api/game/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/game", headers=headers, json=dict(
                steamid=-1,
                name="name",
                short_description="short_description",
                header_image="header_image",
                website="website",
                developers="developers",
                publishers="publishers",
                price="price",
                release_date="release_date",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_game_add_minimal_content(self, test_client, headers, genre_test1):
        """Test game add additional minimal content
        Test:
            POST: /api/game/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/game", headers=headers, json=dict(
                steamid=-2,
                name="name",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_game_add_content_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test game add additional minimal content with bad JWT token
        Test:
            POST: /api/game/
        Expected result: 
            422
        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, to get the access token
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/game", headers=headers_bad, json=dict(
                steamid=-2,
                name="name",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_add_content_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test game add additional minimal content with fake JWT token
        Test:
            POST: /api/game/
        Expected result: 
            404, {"status": False}
        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/game", headers=headers_fake, json=dict(
                steamid=-2,
                name="name",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_add_content_no_jwt(self, test_client, genre_test1):
        """Test game add additional minimal content without JWT token
        Test:
            POST: /api/game/
        Expected result: 
            401, {"status": False}
        Args:
            test_client (app context): Flask application
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/game", json=dict(
                steamid=-2,
                name="name",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### GAME GET ADDITIONAL CONTENT ###
    def test_game_get_additional_content(self, test_client, headers):
        """Test game get additional content
        Test:
            GET: /api/game/additional/
        Expected result: 
            200, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/game/additional", headers=headers)
        res = json.loads(response.data)
        
        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    ### GAME VALIDATE CONTENT ###
    def test_game_validate_additional_content(self, test_client, headers_admin):
        """Test game validate additional content
        Test:
            PUT: /api/game/<int:game_id>
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameAdditionalModel.query.filter_by(steamid=-1).first()
        response = test_client.put("/api/game/additional/"+str(game.game_id), headers=headers_admin)

        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

        
    ### GAME DECLINE CONTENT ###
    def test_game_decline_additional_content(self, test_client, headers_admin):
        """Test game validate decline content
        Test:
            DELETE: /api/game/<int:game_id>
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        game = GameAdditionalModel.query.filter_by(steamid=-2).first()
        response = test_client.delete("/api/game/additional/"+str(game.game_id), headers=headers_admin)

        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True