from src import service
from src.utils import err_resp, message, internal_err_resp, Spotify, validation_error
from src.model import UserModel, ExternalModel, TrackModel, MetaUserTrackModel
from src import db
from flask import current_app
from flask_jwt_extended import create_access_token, decode_token

import dateutil.parser
import sys


class ExternalService:
    @staticmethod
    def get_spotify_oauth(user_uuid):
        """ Get spotify oauth url """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if (external := ExternalModel.query.filter_by(user_id=user.user_id,service_name="Spotify").first()) is None:
                resp = message(True, "Spotify oauth url sent")
                resp["spotify_url"] = Spotify.oauth_url(user_uuid)
            else:
                resp = message(True, "Spotify is already linked")
                resp["spotify_url"] = 'linked'
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def spotify_callback(csrf, code, user_uuid):
        """ Store Spotify access and refresh token """
        if decode_token(csrf)['identity'] != user_uuid:
            return err_resp("CSRF invalid!", 404)
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        # Check if the email is taken
        if ExternalModel.query.filter_by(user_id=user.user_id,service_name="Spotify").first() is not None:
            return validation_error(False, "Spotify Oauth is already done.")
        try:
            token_info = Spotify.get_tokens(code)

            new_external = ExternalModel(
                service_name='Spotify',
                user_id=user.user_id,
                access_token=token_info['access_token'],
                refresh_token=token_info['refresh_token']
            )

            db.session.add(new_external)
            db.session.flush()

            # Commit changes to DB
            db.session.commit()

            resp = message(True, "Spotify tokens stored")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_spotify_data(user_uuid, app):
        """ Get spotify data :  """
        with app.app_context():
            if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
                return err_resp("User not found!", 404)
            if not (external := ExternalModel.query.filter_by(user_id=user.user_id,service_name="Spotify").first()):
                return err_resp("External service not found!", 404)
            try:
                token_info = Spotify.refresh_token(external.refresh_token)
                external.access_token = token_info['access_token']

                db.session.add(external)

                db.session.commit()
                data = []

                data.append(Spotify.get_user_top_track(external.access_token))
                data.append(Spotify.get_user_recently_played(
                    external.access_token))
                for item in Spotify.get_user_playlist(external.access_token):
                    data.append(item['tracks'])

                for d in data:
                    for line in d:
                        if TrackModel.query.filter_by(spotify_id=line['spotify_id']).first() is None:
                            new_track = TrackModel(
                                artist_name=" & ".join(line['artist_name']),
                                title=line['title'],
                                year=line['year'].split("-")[0] if line['year'] is not None else None,
                                release=line['release'],
                                spotify_id=line['spotify_id'],
                                covert_art_url=line['cover_art_url']
                            )
                            db.session.add(new_track)
                            db.session.flush()
                db.session.commit()

                for d in data:
                    for line in d:
                        track = TrackModel.query.filter_by(
                            spotify_id=line['spotify_id']).first()
                        if ((meta := MetaUserTrackModel.query.filter_by(track_id=track.track_id).first()) is None):
                            new_meta_user_track = MetaUserTrackModel(
                                user_id=user.user_id,
                                track_id=track.track_id,
                                play_count=1,
                                last_played_date=dateutil.parser.isoparse(
                                    line['played_at'][:-1]) if "played_at" in line.keys() else None
                            )
                            db.session.add(new_meta_user_track)
                            db.session.flush()
                db.session.commit()

            except Exception as error:
                current_app.logger.error(error)
                return internal_err_resp()
