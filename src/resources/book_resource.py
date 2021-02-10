import uuid
from flask import request
from flask_restx import Resource, reqparse
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

    book_additional = BookDto.book_additional_base

    @api.doc(
        "Add additional Book for validation",
        responses={
            200: ("Additional book added for validation", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(book_additional, validate=True)
    def post(self):
        """ Add additional Book for validation"""
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return BookService.add_additional_book(user_uuid, data)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class BookUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended books for the connected user",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended books for the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return BookService.get_recommended_books_for_user(args["page"], user_uuid, args["reco_engine"])


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class BookGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended books for the groups of the connected user",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended books for the groups of the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return BookService.get_recommended_books_for_group(args["page"], user_uuid, args["reco_engine"])


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
    bad_recommendation = BookDto.book_bad_recommendation

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

class BookAdditionalResource(Resource):
    @api.doc(
        "Get list of the added Books (by user)",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the added Books (by user) """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()

        return BookService.get_additional_book(user_uuid, args["page"])


@api.route("/additional/<int:book_id>")
class BookAdditionalResource(Resource):
    @api.doc(
        "Validate (put) added Books (by user)",
        responses={
            201: ("Additional book data successfully validated"),
            401: ("Authentication required"),
            404: ("User or book not found!"),
        },
    )
    @jwt_required
    def put(self, book_id):
        """ Validate (put) added Books (by user) """
        user_uuid = get_jwt_identity()

        return BookService.validate_additional_book(user_uuid, book_id)

    @api.doc(
        "Decline (delete) added Books (by user)",
        responses={
            201: ("Additional book successfully deleted"),
            401: ("Authentication required"),
            404: ("User or book not found!"),
        },
    )
    @jwt_required
    def delete(self, book_id):
        """ Decline (delete) added Books (by user) """
        user_uuid = get_jwt_identity()

        return BookService.decline_additional_book(user_uuid, book_id)