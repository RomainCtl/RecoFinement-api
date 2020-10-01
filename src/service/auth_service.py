from flask import current_app, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies

from src import db
from src.utils import message, err_resp, internal_err_resp, validation_error
from src.model import UserModel, RevokedTokenModel
from src.schemas import UserBase

user_base = UserBase()


class AuthService:
    @staticmethod
    def login(data):
        # Assign vars
        email = data["email"]
        password = data["password"]

        try:
            # Fetch user data
            if not (user := UserModel.query.filter_by(email=email).first()):
                return err_resp(
                    "Failed to log in.",
                    401,
                )

            elif user and user.verify_password(password):
                user_info = user_base.dump(user)

                access_token = create_access_token(identity=user.uuid)

                resp = message(True, "Successfully logged in.")
                resp["user"] = user_info
                resp["access_token"] = access_token

                return resp, 200

            return err_resp(
                "Failed to log in.", 401
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
        if UserModel.query.filter_by(email=email).first() is not None:
            return validation_error(False, "Email is already being used.")

        try:
            new_user = UserModel(
                email=email,
                username=username,
                password=password,
            )

            db.session.add(new_user)
            db.session.flush()

            # Load the new user's info
            user_info = user_base.dump(new_user)

            # Commit changes to DB
            db.session.commit()

            # Create an access token
            access_token = create_access_token(identity=new_user.uuid)

            resp = message(True, "User has been registered.")
            resp["user"] = user_info
            resp["access_token"] = access_token

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def logout(data):
        jti = data['jti']
        try:
            resp = make_response("", 204)
            unset_jwt_cookies(resp)

            revoked_token = RevokedTokenModel(jti=jti)

            db.session.add(revoked_token)
            db.session.commit()

            return resp
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
