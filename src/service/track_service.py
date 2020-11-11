from flask import current_app
from sqlalchemy import func, text, and_
from datetime import datetime

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import TrackModel, MetaUserTrackModel, GenreModel, ContentType, UserModel
from src.schemas import TrackBase, TrackObject, GenreBase, MetaUserTrackBase


class TrackService:
    @staticmethod
    def search_track_data(search_term, page):
        """ Search track data by title """
        tracks, total_pages = Paginator.get_from(
            TrackModel.query.filter(TrackModel.title.ilike(search_term+"%")).union(
                TrackModel.query.filter(TrackModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            track_data = TrackObject.loads(tracks)

            return pagination_resp(
                message="Track data sent",
                content=track_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_most_popular_tracks(page):
        # NOTE IMDB measure of popularity does not seem to be relevant for this media.
        tracks, total_pages = Paginator.get_from(
            TrackModel.query.order_by(
                TrackModel.rating_count.desc().nullslast(),
                TrackModel.rating.desc().nullslast(),
            ),
            page,
        )

        try:
            track_data = TrackObject.loads(tracks)

            return pagination_resp(
                message="Most popular track data sent",
                content=track_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_ordered_genre():
        genres = GenreModel.query.filter_by(
            content_type=ContentType.TRACK).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "track genres data sent")
            resp["content"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_meta(user_uuid, track_id):
        """ Get specific 'meta_user_track' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if not (meta_user_track := MetaUserTrackModel.query.filter_by(user_id=user.user_id, track_id=track_id).first()):
                meta_user_track = MetaUserTrackModel(
                    track_id=track_id, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_track.review_see_count += 1
            db.session.add(meta_user_track)
            db.session.commit()

            meta_user_track_data = MetaUserTrackBase.load(meta_user_track)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_track_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, track_id, data):
        """ Add 'additional_play_count' to 'play_count' or/and update 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (track := TrackModel.query.filter_by(track_id=track_id).first()):
            return err_resp("Track not found!", 404)

        try:
            if not (meta_user_track := MetaUserTrackModel.query.filter_by(user_id=user.user_id, track_id=track_id).first()):
                meta_user_track = MetaUserTrackModel(
                    track_id=track_id, user_id=user.user_id, play_count=0)

            if 'rating' in data:
                # Update average rating on object
                track.rating = track.rating or 0
                track.rating_count = track.rating_count or 0
                count = track.rating_count + \
                    (1 if meta_user_track.rating is None else 0)
                track.rating = (track.rating * track.rating_count - (
                    meta_user_track.rating if meta_user_track.rating is not None else 0) + data["rating"]) / count
                track.rating_count = count

                meta_user_track.rating = data["rating"]
            if 'additional_play_count' in data:
                meta_user_track.play_count += data['additional_play_count']
                meta_user_track.last_played_date = datetime.now()

            db.session.add(meta_user_track)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_history(user_uuid, page):
        """ Get the history of listened track """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        datas, total_pages = Paginator.get_from(
            db.session.query(MetaUserTrackModel, TrackModel)
            .select_from(MetaUserTrackModel)
            .outerjoin(TrackModel, TrackModel.track_id == MetaUserTrackModel.track_id)
            .filter(and_(MetaUserTrackModel.user_id == user.user_id, MetaUserTrackModel.last_played_date != None))
            .order_by(
                MetaUserTrackModel.last_played_date.desc()
            ),
            page,
        )

        try:
            history_data = list(map(lambda x: {
                                "last_played_date": MetaUserTrackBase.load(x[0])["last_played_date"],
                                "track": TrackObject.load(x[1])
                                }, datas))

            return pagination_resp(
                message="History of listened track data successfully updated",
                content=history_data,
                page=page,
                total_pages=total_pages
            )
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
