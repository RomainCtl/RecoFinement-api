import pytest
import json
from src.model import GameModel, MetaUserGameModel
from src import db

class TestGame:

    ### GAME RESOURCE ###

    def test_game_recommended(self, test_client, headers):
        if not (GameModel.query.filter_by(game_id=999999).first()):
            new_game = GameModel(
                game_id = 999999,
                steamid = 999999,
                name="test game",
                short_description="short desc game",
                rating=5.0,
                header_image="header img",
                website= "website",
                developers="dev",
                publishers = "publishers",
                price = "free",
                recommendations = 150,
                release_date = "11/10/2020",
                rating_count = 10
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
        response = test_client.get("/api/game?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []
    
    def test_game_recommended_big_page(self, test_client, headers):
        response = test_client.get("/api/game?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_game_recommended_zero_page(self, test_client, headers):
        response = test_client.get("/api/game?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_recommended_negative_page(self, test_client, headers):
        response = test_client.get("/api/game?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_game_recommended_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/game", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_recommended_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/game", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_game_recommended_no_jwt(self, test_client):
        response = test_client.get("/api/game")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### GAME SEARCH ###

    def test_game_search(self, test_client, headers):
        response = test_client.get("/api/game/search/test%20game", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_game_search_one_page(self, test_client, headers):
        response = test_client.get("/api/game/search/test%20game?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_game_search_zero_page(self, test_client, headers):
        response = test_client.get("/api/game/search/test%20game?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_game_search_big_page(self, test_client, headers):
        response = test_client.get("/api/game/search/test%20game?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_game_search_negative_page(self, test_client, headers):
        response = test_client.get("/api/game/search/test%20game?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_game_search_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/game/search/test%20game", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_search_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/game/search/test%20game", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_game_search_no_jwt(self, test_client):
        response = test_client.get("/api/game/search/test%20game")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### GAME GENRE ###

    def test_game_genre(self, test_client, headers):
        response = test_client.get("/api/game/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_game_genre_no_jwt(self, test_client):
        response = test_client.get("/api/game/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_game_genre_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/game/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_genre_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/game/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### GAME USER META ###

    def test_game_user_meta(self, test_client, headers):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.get("/api/game/"+str(game.game_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_game_user_meta_bad_game_id(self, test_client, headers):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.get("/api/game/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_bad_jwt(self, test_client, headers_bad):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.get("/api/game/"+str(game.game_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_user_meta_fake_jwt(self, test_client, headers_fake):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.get("/api/game/"+str(game.game_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_no_jwt(self, test_client):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.get("/api/game/"+str(game.game_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### GAME USER META UPDATE ###
    
    def test_game_user_meta_update(self, test_client, headers, user_test1):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.game_id)+"/meta", headers=headers, json=dict(
            rating = 5,
            purchase = True,
            additional_hours = 24.0
        ))
        
        res = json.loads(response.data)
        meta = MetaUserGameModel.query.filter_by(user_id=user_test1.user_id,game_id=999999).first()


        assert response.status_code == 201
        assert res['status'] == True
        assert meta.purchase == True
        assert meta.rating == 5
        assert meta.hours == 24.0

    def test_game_user_meta_update_bad_game_id(self, test_client, headers):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.patch("/api/game/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_hours=24.5,
            purchase = True
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_update_bad_jwt(self, test_client, headers_bad):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.game_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_hours=24.5,
            purchase = True
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_game_user_meta_update_fake_jwt(self, test_client, headers_fake):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.game_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_hours=24.5,
            purchase = True
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_game_user_meta_update_no_jwt(self, test_client):
        game = GameModel.query.filter_by(game_id=999999).first()
        response = test_client.patch("/api/game/"+str(game.game_id)+"/meta", json=dict(
            rating=5,
            additional_hours=24.5,
            purchase = True
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
