import uuid
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import BookService, ContentService
from src.dto import BookDto, UserDto

api = BookDto.api
data_resp = BookDto.data_resp
meta_resp = UserDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class BookResource(Resource):
    @api.doc(
        "Get list of the most popular Books",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Books """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return BookService.get_popular_books(page, user_uuid)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class BookUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended books for the connected user",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended books for the connected user """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return BookService.get_recommended_books_for_user(page, user_uuid)


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class BookGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended books for the groups of the connected user",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended books for the groups of the connected user """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return BookService.get_recommended_books_for_group(page, user_uuid)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class BookSearchResource(Resource):
    @api.doc(
        "Search books",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of book's data by term """
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        uuid = get_jwt_identity()
        return BookService.search_book_data(search_term, page, uuid)


@api.route("/<int:content_id>/meta")
class bookMetaResource(Resource):
    @api.doc(
        "Get book-user (connected user) meta",
        responses={
            200: ("Book-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get book-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ContentService.get_meta(user_uuid, content_id)

    content_meta = UserDto.content_meta

    @api.doc(
        "Update book-user (connected user) meta",
        responses={
            201: ("Book-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Book not found!",
        },
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def patch(self, content_id):
        """ Update book-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ContentService.update_meta(user_uuid, content_id, data)


@api.route("/<int:content_id>/bad_recommendation")
class BookBadRecommendation(Resource):
    bad_recommendation = UserDto.bad_recommendation

    @api.doc(
        "Add Book-user (connected user) bad recommendation",
        responses={
            200: ("Book-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, content_id):
        """ Add Book-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return BookService.add_bad_recommendation(user_uuid, content_id, data)
