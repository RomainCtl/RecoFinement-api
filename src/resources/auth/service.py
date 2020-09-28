from flask import current_app, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

from src import db
from src.utils import message, err_resp, internal_err_resp, validation_error
from src.model import User, RevokedToken
from src.schemas import UserSchema

user_schema = UserSchema()


class AuthService:
    @staticmethod
    def login(data):
        # Assign vars
        email = data["email"]
        password = data["password"]

        try:
            # Fetch user data
            if not (user := User.query.filter_by(email=email).first()):
                return err_resp(
                    "Failed to log in.",
                    "invalid_auth",
                    401,
                )

            elif user and user.verify_password(password):
                user_info = user_schema.dump(user)

                access_token = create_access_token(identity=user.uuid)

                resp = message(True, "Successfully logged in.")
                resp["user"] = user_info

                resp = make_response(jsonify(**resp), 200)
                set_access_cookies(resp, access_token)

                return resp

            return err_resp(
                "Failed to log in.", "invalid_auth", 401
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def register(data):
        # Assign vars

        # Required values
        email = data["email"]
        username = data["username"]
        password = data["password"]

        # Check if the email is taken
        if User.query.filter_by(email=email).first() is not None:
            return validation_error(False, ["Email is already being used."]), 400

        try:
            new_user = User(
                email=email,
                username=username,
                password=password,
            )

            db.session.add(new_user)
            db.session.flush()

            # Load the new user's info
            user_info = user_schema.dump(new_user)

            # Commit changes to DB
            db.session.commit()

            # Create an access token
            access_token = create_access_token(identity=new_user.uuid)

            resp = message(True, "User has been registered.")
            resp["user"] = user_info

            resp = make_response(jsonify(**resp), 201)
            set_access_cookies(resp, access_token)

            return resp

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def logout(data):
        jti = data['jti']
        try:
            resp = make_response("", 204)
            unset_jwt_cookies(resp)

            revoked_token = RevokedToken(jti=jti)

            db.session.add(revoked_token)
            db.session.commit()

            return resp
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
