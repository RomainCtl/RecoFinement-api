from flask import current_app
from flask_jwt_extended import create_access_token

from src import db
from src.utils import message, err_resp, internal_err_resp
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
                resp["access_token"] = access_token
                resp["user"] = user_info

                return resp, 200

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
            return err_resp("Email is already being used.", "email_taken", 400)

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
            resp["access_token"] = access_token
            resp["user"] = user_info

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def logout(data):
        jti = data['jti']
        try:
            revoked_token = RevokedToken(jti=jti)

            db.session.add(revoked_token)
            db.session.commit()

            return "", 204
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
