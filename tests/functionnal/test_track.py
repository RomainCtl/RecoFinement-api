import pytest
import json
from src.model import TrackModel, MetaUserTrackModel
from src import db
import uuid

class TestApplication:

    ### SERIE RESOURCE ###

    def test_track_recommended(self, test_client, headers):
        if not (TrackModel.query.filter_by(track_id=999999).first()):
            new_track = TrackModel(
                track_id = 999999,
                title="test track",
                year=2020,
                artist_name="artist track",
                release="24/12/2019",
                track_mmid= "99999999",
                recording_mbid=uuid.uuid4(),
                rating = 4.0,
                rating_count = 1000,
                spotify_id = "999999999",
                covert_art_url = "cover",
            )
            db.session.add(new_track)
            db.session.flush()
            db.session.commit()
        response = test_client.get("/api/track", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_track_recommended_one_page(self, test_client, headers):
        response = test_client.get("/api/track?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []
    
    def test_track_recommended_big_page(self, test_client, headers):
        response = test_client.get("/api/track?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_track_recommended_zero_page(self, test_client, headers):
        response = test_client.get("/api/track?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_recommended_negative_page(self, test_client, headers):
        response = test_client.get("/api/track?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_track_recommended_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/track", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_recommended_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/track", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_track_recommended_no_jwt(self, test_client):
        response = test_client.get("/api/track")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### SERIE SEARCH ###

    def test_track_search(self, test_client, headers):
        response = test_client.get("/api/track/search/test%20track", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_track_search_one_page(self, test_client, headers):
        response = test_client.get("/api/track/search/test%20track?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_track_search_zero_page(self, test_client, headers):
        response = test_client.get("/api/track/search/test%20track?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_track_search_big_page(self, test_client, headers):
        response = test_client.get("/api/track/search/test%20track?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []
    
    def test_track_search_negative_page(self, test_client, headers):
        response = test_client.get("/api/track/search/test%20track?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_search_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/track/search/test%20track", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_search_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/track/search/test%20track", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    def test_track_search_no_jwt(self, test_client):
        response = test_client.get("/api/track/search/test%20track")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### SERIE GENRE ###

    def test_track_genre(self, test_client, headers):
        response = test_client.get("/api/track/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_track_genre_no_jwt(self, test_client):
        response = test_client.get("/api/track/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    def test_track_genre_bad_jwt(self, test_client, headers_bad):
        response = test_client.get("/api/track/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_genre_fake_jwt(self, test_client, headers_fake):
        response = test_client.get("/api/track/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False
    
    ### SERIE USER META ###

    def test_track_user_meta(self, test_client, headers):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.get("/api/track/"+str(track.track_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_track_user_meta_bad_track_id(self, test_client, headers):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.get("/api/track/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_bad_jwt(self, test_client, headers_bad):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.get("/api/track/"+str(track.track_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_user_meta_fake_jwt(self, test_client, headers_fake):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.get("/api/track/"+str(track.track_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_no_jwt(self, test_client):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.get("/api/track/"+str(track.track_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
    
    ### SERIE USER META UPDATE ###
    
    def test_track_user_meta_update(self, test_client, headers, user_test1):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.track_id)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_play_count=5
            
        ))
        res = json.loads(response.data)
        meta = MetaUserTrackModel.query.filter_by(user_id=user_test1.user_id,track_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.play_count == 5
        assert meta.rating == 5

    def test_track_user_meta_update_bad_track_id(self, test_client, headers):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.patch("/api/track/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_play_count=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_update_bad_jwt(self, test_client, headers_bad):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.track_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_play_count=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_user_meta_update_fake_jwt(self, test_client, headers_fake):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.track_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_play_count=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_update_no_jwt(self, test_client):
        track = TrackModel.query.filter_by(track_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.track_id)+"/meta", json=dict(
            rating=5,
            additional_play_count=5
            
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"
