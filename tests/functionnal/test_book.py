import pytest
import json
from src.model import BookModel, ContentModel, MetaUserContentModel
from src import db


class TestBook:

    ### BOOK RESOURCE ###

    def test_book_recommended(self, test_client, headers):
        """Test book recommended

        Test:
            GET: /api/book

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP headers, to get the access token
        """
        if not (BookModel.query.filter_by(content_id=999999).first()):
            content = ContentModel(
                content_id=999999, rating=5.0, rating_count=10000)
            db.session.add(content)
            db.session.flush()
            new_book = BookModel(
                isbn="123456789012",
                title="test book",
                author="test author",
                year_of_publication=2020,
                publisher="publisher test",
                image_url_s="110k",
                image_url_m="chat",
                image_url_l="free",
                content=content,
            )
            db.session.add(new_book)
            db.session.flush()
            db.session.commit()

        response = test_client.get("/api/book", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_book_recommended_one_page(self, test_client, headers):
        """Test book get recommended book page 1

        Test:
            GET: /api/book?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/book?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_book_recommended_big_page(self, test_client, headers):
        """Test book get recommended book page 9999999

        Test:
            GET: /api/book?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/book?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_book_recommended_zero_page(self, test_client, headers):
        """Test book get recommended book page 0

        Test:
            GET: /api/book?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/book?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_book_recommended_negative_page(self, test_client, headers):
        """Test book get recommended book page -1

        Test:
            GET: /api/book?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get("/api/book?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_book_recommended_bad_jwt(self, test_client, headers_bad):
        """Test book get recommended book with bad JWT token 

        Test:
            GET: /api/book

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            header_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get("/api/book", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_book_recommended_fake_jwt(self, test_client, headers_fake):
        """Test book get recommended book with fake JWT token 

        Test:
            GET: /api/book

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get("/api/book", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_recommended_no_jwt(self, test_client):
        """Test book get recommended book without JWT token 

        Test:
            GET: /api/book

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/book")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### BOOK SEARCH ###

    def test_book_search(self, test_client, headers):
        """Test book search

        Test:
            GET: /api/book/search/test book

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/book/search/test%20book", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_book_search_one_page(self, test_client, headers):
        """Test book search get page 1

        Test:
            GET: /api/book/search/test book?page=1

        Expected result: 
            200, {"status": True, "content": ResponseObject}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/book/search/test%20book?page=1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] != []

    def test_book_search_zero_page(self, test_client, headers):
        """Test book search get page 0

        Test:
            GET: /api/book/search/test book?page=0

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/book/search/test%20book?page=0", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_book_search_big_page(self, test_client, headers):
        """Test book search get page 9999999

        Test:
            GET: /api/book/search/test book?page=9999999

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/book/search/test%20book?page=9999999", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_book_search_negative_page(self, test_client, headers):
        """Test book search get page -1

        Test:
            GET: /api/book/search/test book?page=-1

        Expected result: 
            200, {"status": True, "content": []}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/book/search/test%20book?page=-1", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True
        assert res['content'] == []

    def test_book_search_bad_jwt(self, test_client, headers_bad):
        """Test book search with bad JWT token 

        Test:
            GET: /api/book/search/test book

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        response = test_client.get(
            "/api/book/search/test%20book", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_book_search_fake_jwt(self, test_client, headers_fake):
        """Test book search with fake JWT token 

        Test:
            GET: /api/book/search/test book

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        response = test_client.get(
            "/api/book/search/test%20book", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_search_no_jwt(self, test_client):
        """Test book search without JWT token

        Test:
            GET: /api/book/search/test book

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        response = test_client.get("/api/book/search/test%20book")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### BOOK USER META ###

    def test_book_user_meta(self, test_client, headers):
        """Test book user meta

        Test:
            GET: /api/book/<content_id>/meta

        Expected result: 
            200, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/book/"+str(book.content_id)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 200
        assert res['status'] == True

    def test_book_user_meta_bad_content_id(self, test_client, headers):
        """Test book user meta with bad content_id

        Test:
            GET: /api/book/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.get(
            "/api/book/"+str(999999999999)+"/meta", headers=headers)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_user_meta_bad_jwt(self, test_client, headers_bad):
        """Test book user meta with bad JWT token 

        Test:
            GET: /api/book/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/book/"+str(book.content_id)+"/meta", headers=headers_bad)
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_book_user_meta_fake_jwt(self, test_client, headers_fake):
        """Test book user meta with fake JWT token 

        Test:
            GET: /api/book/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.get(
            "/api/book/"+str(book.content_id)+"/meta", headers=headers_fake)
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_user_meta_no_jwt(self, test_client):
        """Test book user mate without JWT token

        Test:
            GET: /api/book/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.get("/api/book/"+str(book.content_id)+"/meta")
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### BOOK USER META UPDATE ###

    def test_book_user_meta_update(self, test_client, headers, user_test1):
        """Test book user meta update

        Test:
            PATCH: /api/book/<content_id>/meta

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
            user_test1 (User object): user test1
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/book/"+str(book.content_id)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=1
        ))
        res = json.loads(response.data)
        meta = MetaUserContentModel.query.filter_by(
            user_id=user_test1.user_id, content_id=999999).first()

        assert response.status_code == 201
        assert res['status'] == True
        assert meta.count == 1
        assert meta.rating == 5

    def test_book_user_meta_update_bad_content_id(self, test_client, headers):
        """Test book user meta update with bad content_id

        Test:
            PATCH: /api/book/<bad_content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/book/"+str(999999999)+"/meta", headers=headers, json=dict(
            rating=5,
            additional_count=1

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_user_meta_update_bad_jwt(self, test_client, headers_bad):
        """Test book user meta update with bad JWT token 

        Test:
            PATCH: /api/book/<content_id>/meta

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers_bad (dict): bad HTTP header, with bad access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/book/"+str(book.content_id)+"/meta", headers=headers_bad, json=dict(
            rating=5,
            additional_count=1

        ))
        res = json.loads(response.data)

        assert response.status_code == 422

    def test_book_user_meta_update_fake_jwt(self, test_client, headers_fake):
        """Test book user meta update with fake JWT token 

        Test:
            PATCH: /api/book/<content_id>/meta

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers_fake (dict): fake HTTP header, with invalid signed access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/book/"+str(book.content_id)+"/meta", headers=headers_fake, json=dict(
            rating=5,
            additional_count=1

        ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_user_meta_update_no_jwt(self, test_client):
        """Test book user meta update without JWT token 

        Test:
            PATCH: /api/book/<content_id>/meta

        Expected result: 
            401, {"msg" : "Missing Authorization Header"}

        Args:
            test_client (app context): Flask application
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.patch("/api/book/"+str(book.content_id)+"/meta", json=dict(
            rating=5,
            additional_count=1
        ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"

    ### BOOK BAD RECOMMENDATION ###

    def test_book_bad_recommendation(self, test_client, headers):
        """Test book bad recommendation

        Test:
            GET: /api/book/<int:content_id>/bad_recommendation

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/book/"+str(book.content_id)+"/bad_recommendation", headers=headers, json=dict(
                year_of_publication=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True

    def test_book_bad_recommendation_bad_content_id(self, test_client, headers):
        """Test book bad recommendation with bad book ID

        Test:
            GET: /api/book/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        response = test_client.post(
            "/api/book/"+str(999999999)+"/bad_recommendation", headers=headers, json=dict(
                year_of_publication=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_bad_recommendation_bad_jwt(self, test_client, headers_bad):
        """Test book bad recommendation with bad JWT token

        Test:
            GET: /api/book/<int:content_id>/bad_recommendation

        Expected result: 
            422

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """
        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/book/"+str(book.content_id)+"/bad_recommendation", headers=headers_bad, json=dict(
                year_of_publication=["2010"]
            ))
        #res = json.loads(response.data)

        assert response.status_code == 422

    def test_book_bad_recommendation_fake_jwt(self, test_client, headers_fake):
        """Test book bad recommendation with fake JWT token

        Test:
            GET: /api/book/<int:content_id>/bad_recommendation

        Expected result: 
            404, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/book/"+str(book.content_id)+"/bad_recommendation", headers=headers_fake, json=dict(
                year_of_publication=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 404
        assert res['status'] == False

    def test_book_bad_recommendation_no_jwt(self, test_client):
        """Test book bad recommendation without JWT token

        Test:
            GET: /api/book/<int:content_id>/bad_recommendation

        Expected result: 
            401, {"status": False}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        book = BookModel.query.filter_by(content_id=999999).first()
        response = test_client.post(
            "/api/book/"+str(book.content_id)+"/bad_recommendation", json=dict(
                year_of_publication=["2010"]
            ))
        res = json.loads(response.data)

        assert response.status_code == 401
        assert res['msg'] == "Missing Authorization Header"


    ### BOOK ADD CONTENT ###
    def test_book_add_content(self, test_client, headers):
        """Test book add additional content

        Test:
            POST: /api/book/

        Expected result: 
            201, {"status": True}

        Args:
            test_client (app context): Flask application
            headers (dict): HTTP header, to get the access token
        """

        response = test_client.post(
            "/api/book", headers=headers, json=dict(
                isbn="isbn",
                title="title",
                author="author",
                year_of_publication=1900,
                publisher="publisher",
                image_url_s="image_url_s",
                image_url_m="image_url_m",
                image_url_l="image_url_l"
            ))
        res = json.loads(response.data)

        assert response.status_code == 201
        assert res['status'] == True
