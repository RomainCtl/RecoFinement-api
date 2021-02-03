import pytest
import json
from src.model import TrackModel, ContentModel, MetaUserContentModel
from src import db
import uuid


class TestTrack:

    ### TRACK RESOURCE ###

    def test_track_recommended(self, test_client, headers):
        """Test track recommended

        Test:
            GET: /api/track

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        if not (TrackModel.query.filter_by(content_id=999999).first()):
            content = ContentModel(
                content_id=999999, rating=4.0, rating_count=1000)
            db.session.add(content)
            db.session.flush()
            new_track = TrackModel(
                title="test track",
                year=2020,
                artist_name="artist track",
                release="24/12/2019",
                track_mmid="99999999",
                recording_mbid=uuid.uuid4(),
                spotify_id="999999999",
                covert_art_url="cover",
                content=content
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
        """Test track get recommended track page 1

        Test:
            GET: /api/track?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/track?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_track_recommended_big_page(self, test_client, headers):
        """Test track get recommended track page 9999999

        Test:
            GET: /api/track?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/track?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_recommended_zero_page(self, test_client, headers):
        """Test track get recommended track page 0

        Test:
            GET: /api/track?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/track?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_recommended_negative_page(self, test_client, headers):
        """Test track get recommended track page -1

        Test:
            GET: /api/track?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/track?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_recommended_bad_jwt(self, test_client, headers_bad):
        """Test track get recommended track with bad JWT token 

        Test:
            GET: /api/track

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            header_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/track", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_recommended_fake_jwt(self, test_client, headers_fake):
        """Test track get recommended track with fake JWT token 

        Test:
            GET: /api/track

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/track", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_recommended_no_jwt(self, test_client):
        """Test track get recommended track without JWT token 

        Test:
            GET: /api/track

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/track")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### TRACK SEARCH ###

    def test_track_search(self, test_client, headers):
        """Test track search

        Test:
            GET: /api/track/search/test track

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/track/search/test%20track", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_track_search_one_page(self, test_client, headers):
        """Test track search get page 1

        Test:
            GET: /api/track/search/test track?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/track/search/test%20track?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_track_search_zero_page(self, test_client, headers):
        """Test track search get page 0

        Test:
            GET: /api/track/search/test track?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/track/search/test%20track?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_search_big_page(self, test_client, headers):
        """Test track search get page 9999999

        Test:
            GET: /api/track/search/test track?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/track/search/test%20track?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_search_negative_page(self, test_client, headers):
        """Test track search get page -1

        Test:
            GET: /api/track/search/test track?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/track/search/test%20track?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_track_search_bad_jwt(self, test_client, headers_bad):
        """Test track search with bad JWT token 

        Test:
            GET: /api/track/search/test track

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get(
            "/api/track/search/test%20track", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_search_fake_jwt(self, test_client, headers_fake):
        """Test track search with fake JWT token 

        Test:
            GET: /api/track/search/test track

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get(
            "/api/track/search/test%20track", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_search_no_jwt(self, test_client):
        """Test track search without JWT token

        Test:
            GET: /api/track/search/test track

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/track/search/test%20track")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### TRACK GENRE ###

    def test_track_genre(self, test_client, headers):
        """Test track genre

        Test:
            GET: /api/track/genres

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/track/genres", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_track_genre_no_jwt(self, test_client):
        """Test track genre whithout JWT token

        Test:
            GET: /api/track/genres

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/track/genres")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    def test_track_genre_bad_jwt(self, test_client, headers_bad):
        """Test track genre with bad JWT token 

        Test:
            GET: /api/track/genres

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/track/genres", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_genre_fake_jwt(self, test_client, headers_fake):
        """Test track genre with fake JWT token 

        Test:
            GET: /api/track/genres

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/track/genres", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    ### TRACK USER META ###

    def test_track_user_meta(self, test_client, headers):
        """Test track user meta

        Test:
            GET: /api/track/<content_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/track/"+str(track.content_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_track_user_meta_bad_content_id(self, test_client, headers):
        """Test track user meta with bad content_id

        Test:
            GET: /api/track/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/track/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test track user meta with bad JWT token 

        Test:
            GET: /api/track/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/track/"+str(track.content_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test track user meta with fake JWT token 

        Test:
            GET: /api/track/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/track/"+str(track.content_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_no_jwt(self, test_client):
        """Test track user mate without JWT token

        Test:
            GET: /api/track/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.get("/api/track/"+str(track.content_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### TRACK USER META UPDATE ###

    def test_track_user_meta_update(self, test_client, headers, user_test1):
        """Test track user meta update

        Test:
            PATCH: /api/track/<content_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.content_id)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=5
        ))
        res = json.loads(response.data)
        meta = MetaUserContentModel.query.filter_by(
            user_id=user_test1.user_id, content_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.count == 5  # play_count
        assert meta.rating == 5

    def test_track_user_meta_update_bad_content_id(self, test_client, headers):
        """Test track user meta update with bad content_id

        Test:
            PATCH: /api/track/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.patch("/api/track/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test track user meta update with bad JWT token 

        Test:
            PATCH: /api/track/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.content_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_count=5

        ))
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test track user meta update with fake JWT token 

        Test:
            PATCH: /api/track/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.content_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_count=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_user_meta_update_no_jwt(self, test_client):
        """Test track user meta update without JWT token 

        Test:
            PATCH: /api/track/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/track/"+str(track.content_id)+"/meta", json=dict(
            rating=5,
            additional_count=5

        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### TRACK BAD RECOMMENDATION ###

    def test_track_bad_recommendation(self, test_client, headers):
        """Test track bad recommendation

        Test:
            GET: /api/track/<int:content_id>/bad_recommendation

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/track/"+str(track.content_id)+"/bad_recommendation", headers=headers, json=dict(
                year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_track_bad_recommendation_bad_content_id(self, test_client, headers):
        """Test track bad recommendation with bad track ID

        Test:
            GET: /api/track/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.post(
            "/api/track/"+str(999999999)+"/bad_recommendation", headers=headers, json=dict(
                year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_bad_recommendation_bad_jwt(self, test_client, headers_bad):
        """Test track bad recommendation with bad JWT token

        Test:
            GET: /api/track/<int:content_id>/bad_recommendation

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/track/"+str(track.content_id)+"/bad_recommendation", headers=headers_bad, json=dict(
                year=["2010"]
            ))
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_bad_recommendation_fake_jwt(self, test_client, headers_fake):
        """Test track bad recommendation with fake JWT token

        Test:
            GET: /api/track/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/track/"+str(track.content_id)+"/bad_recommendation", headers=headers_fake, json=dict(
                year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_bad_recommendation_no_jwt(self, test_client):
        """Test track bad recommendation without JWT token

        Test:
            GET: /api/track/<int:content_id>/bad_recommendation

        Expected result: 
            401, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        track = TrackModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/track/"+str(track.content_id)+"/bad_recommendation", json=dict(
                year=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"


    ### TRACK ADD CONTENT ###
    def test_track_add_content(self, test_client, headers, genre_test1):
        """Test track add additional content
        Test:
            POST: /api/track/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/track", headers=headers, json=dict(
                title="title",
                year=-1,
                artist_name="artist_name",
                release="release",
                track_mmid="track_mmid",
                recording_mbid="00010203-0405-0607-0809-0a0b0c0d0e0f",
                spotify_id=-1,
                covert_art_url="covert_art_url",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_track_add_minimal_content(self, test_client, headers, genre_test1):
        """Test track add additional minimal content
        Test:
            POST: /api/track/
        Expected result: 
            201, {"status": True}
        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/track", headers=headers, json=dict(
                title="title",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_track_add_content_bad_jwt(self, test_client, headers_bad, genre_test1):
        """Test track add additional minimal content with bad JWT token
        Test:
            POST: /api/track/
        Expected result: 
            422
        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, to get the access token
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/track", headers=headers_bad, json=dict(
                title="title",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_track_add_content_fake_jwt(self, test_client, headers_fake, genre_test1):
        """Test track add additional minimal content with fake JWT token
        Test:
            POST: /api/track/
        Expected result: 
            404, {"status": False}
        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/track", headers=headers_fake, json=dict(
                title="title",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_track_add_content_fake_jwt(self, test_client, genre_test1):
        """Test track add additional minimal content with without JWT token
        Test:
            POST: /api/track/
        Expected result: 
            401, {"status": False}
        Args:
            test_client (app context): Flask application
            genre_test1 (GenreObject) : Genre example
        """

        response = test_client.post(
            "/api/track", json=dict(
                title="title",
                genres=[genre_test1.genre_id],
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"