import pytest
import json
from src.model import SerieModel, MetaUserSerieModel
from src import db

class TestSerie:

    ### SERIE RESOURCE ###

    def test_serie_recommended(self, test_client, headers):
        if not (SerieModel.query.filter_by(serie_id=999999).first()):
            new_serie = SerieModel(
                serie_id = 999999,
                title="test serie",
                rating=5.0,
                actors="authors serie",
                start_year= "2019",
                end_year = "2020",
                directors = "director serie",
                writers = "writer serie",
                imdbid = "99999999",
                rating_count = 1000,
                plot_outline = "plot_outline serie",
                cover = "cover"
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
        response = test_client.get("/api/serie?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []
    
    def test_serie_recommended_big_page(self, test_client, headers):
        response = test_client.get("/api/serie?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_serie_recommended_zero_page(self, test_client, headers):
        response = test_client.get("/api/serie?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_recommended_negative_page(self, test_client, headers):
        response = test_client.get("/api/serie?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_serie_recommended_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/serie", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_recommended_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/serie", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_serie_recommended_no_jwt(self, test_client):
        response = test_client.get("/api/serie")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### SERIE SEARCH ###

    def test_serie_search(self, test_client, headers):
        response = test_client.get("/api/serie/search/test%20serie", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_search_one_page(self, test_client, headers):
        response = test_client.get("/api/serie/search/test%20serie?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_serie_search_zero_page(self, test_client, headers):
        response = test_client.get("/api/serie/search/test%20serie?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_serie_search_big_page(self, test_client, headers):
        response = test_client.get("/api/serie/search/test%20serie?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_serie_search_negative_page(self, test_client, headers):
        response = test_client.get("/api/serie/search/test%20serie?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_serie_search_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/serie/search/test%20serie", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_search_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/serie/search/test%20serie", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_serie_search_no_jwt(self, test_client):
        response = test_client.get("/api/serie/search/test%20serie")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### SERIE GENRE ###

    def test_serie_genre(self, test_client, headers):
        response = test_client.get("/api/serie/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_genre_no_jwt(self, test_client):
        response = test_client.get("/api/serie/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_serie_genre_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/serie/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_genre_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/serie/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### SERIE USER META ###

    def test_serie_user_meta(self, test_client, headers):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_serie_user_meta_bad_serie_id(self, test_client, headers):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get("/api/serie/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_bad_jwt(self, test_client, headers_bad):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_user_meta_fake_jwt(self, test_client, headers_fake):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_no_jwt(self, test_client):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.get("/api/serie/"+str(serie.serie_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### SERIE USER META UPDATE ###
    
    def test_serie_user_meta_update(self, test_client, headers, user_test1):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers, json=dict(
            rating=5,
            num_watched_episodes=5,
            
        ))
        res = json.loads(response.data)
        meta = MetaUserSerieModel.query.filter_by(user_id=user_test1.user_id,serie_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.rating == 5
        assert meta.num_watched_episodes == 5

    def test_serie_user_meta_update_bad_serie_id(self, test_client, headers):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            num_watched_episodes=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_update_bad_jwt(self, test_client, headers_bad):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            num_watched_episodes=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_serie_user_meta_update_fake_jwt(self, test_client, headers_fake):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            num_watched_episodes=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_serie_user_meta_update_no_jwt(self, test_client):
        serie = SerieModel.query.filter_by(serie_id=999999).first()
        response = test_client.patch("/api/serie/"+str(serie.serie_id)+"/meta", json=dict(
            rating=5,
            num_watched_episodes=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
