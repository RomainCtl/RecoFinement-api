from flask import current_app, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, decode_token

import datetime


from src import db
from src.utils import message, err_resp, internal_err_resp, validation_error, mailjet
from src.model import UserModel, RevokedTokenModel
from src.schemas import UserBase
from settings import URL_FRONT

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
            # Send welcome email
            mailjet.sendNewAccount(new_user,URL_FRONT)
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

            revoked_token = RevokedTokenModel(jti=jti)

            db.session.add(revoked_token)
            db.session.commit()

            return resp
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def forget(email,url):
        try:
            # Fetch user data
            if user := UserModel.query.filter_by(email=email).first():

                expires = datetime.timedelta(hours=24)
                reset_token = create_access_token(identity=user.uuid, expires_delta=expires)
                
                user.reset_password_token=reset_token
                mailjet.sendForget(user,URL_FRONT+"reset")
                
                db.session.add(user)
                db.session.commit()
            
            resp = message(True, "If your account exist, you will find an email to recover your password in your mailbox")

            return resp
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def reset(data,url):
        
        reset_token = data['reset_password_token']
        password = data['password']
        uuid = decode_token(reset_token)['identity']
        try:
            # Fetch user data
            if not (user := UserModel.query.filter_by(uuid=uuid).first()):
                return err_resp(
                    "Invalid token.",
                    401,
                )
            
            user.password=password
            if (mailjet.sendReset(user,URL_FRONT) == "error"):
                return make_response("Something went wrong while sending the password reset confirmation email",400)
            
            db.session.add(user)
            db.session.commit()
            resp = message(True, "Password reset successfully")
            return resp

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()