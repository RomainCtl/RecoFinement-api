from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, and_, select
from sqlalchemy.sql.expression import null
from datetime import datetime

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import TrackModel, GenreModel, ContentType, UserModel, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel, TrackAdditionalModel
from src.schemas import TrackBase, TrackObject, GenreBase, TrackExtra, MetaUserContentBase


class TrackService:
    @staticmethod
    def search_track_data(search_term, page, connected_user_uuid):
        """ Search track data by title """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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
    def get_popular_tracks(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # NOTE IMDB measure of popularity does not seem to be relevant for this media.
        tracks, total_pages = Paginator.get_from(
            TrackModel.query.join(TrackModel.content, aliased=True).order_by(
                ContentModel.rating_count.desc().nullslast(),
                ContentModel.rating.desc().nullslast(),
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
    def get_recommended_tracks_for_user(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        tracks, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, TrackModel)
            .join(TrackModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(RecommendedContentModel.user_id == user.user_id)
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                ContentModel.rating_count.desc().nullslast(),
                ContentModel.rating.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                track = TrackExtra.load(row[1])
                track["reco_engine"] = row[0].engine
                track["reco_score"] = row[0].score
                return track

            track_data = list(map(c_load, tracks))

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
    def get_recommended_tracks_for_group(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        tracks, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, TrackModel)
            .join(TrackModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(RecommendedContentForGroupModel.group_id.in_(groups_ids))
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                ContentModel.rating_count.desc().nullslast(),
                ContentModel.rating.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = TrackExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

            track_data = list(map(c_load, tracks))

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
    def get_ordered_genre(connected_user_uuid):
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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
    def get_history(user_uuid, page):
        """ Get the history of listened track """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        datas, total_pages = Paginator.get_from(
            db.session.query(MetaUserContentModel, TrackModel)
            .join(TrackModel.content)
            .join(MetaUserContentModel, MetaUserContentModel.content_id == TrackModel.content_id)
            .filter(and_(MetaUserContentModel.user_id == user.user_id, MetaUserContentModel.last_count_increment != None))
            .order_by(
                MetaUserContentModel.last_count_increment.desc()
            ),
            page,
        )

        try:
            history_data = list(map(lambda x: {
                                "last_played_date": MetaUserContentBase.load(x[0])["last_count_increment"],
                                "track": TrackObject.load(x[1])
                                }, datas))

            return pagination_resp(
                message="History of listened track data successfully updated",
                content=history_data,
                page=page,
                total_pages=total_pages
            )
        except Exception as error:
            import traceback
            traceback.print_exc()
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_bad_recommendation(user_uuid, content_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (track := TrackModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Track not found!", 404)

        try:
            for type, value in data.items():
                if type in REASON_CATEGORIES['track']:
                    for r in value:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id=user.user_id,
                            content_id=track.content_id,
                            reason_categorie=type,
                            reason=r
                        )

                        db.session.add(new_bad_reco)
                        db.session.flush()
            db.session.commit()

            resp = message(True, "Bad recommendation has been registered.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_additional_track(user_uuid, data):
        """ Add additional track"""
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        try:

            new_additional_track = TrackAdditionalModel(
                title=data['title'],
            )

            if 'year' in data :
                new_additional_track.year = data['year']
            if 'artist_name' in data :
                new_additional_track.artist_name = data['artist_name']
            if 'release' in data :
                new_additional_track.release = data['release']
            if 'track_mmid' in data :
                new_additional_track.track_mmid = data['track_mmid']
            if 'recording_mbid' in data :
                new_additional_track.recording_mbid = data['recording_mbid']
            if 'spotify_id' in data :
                new_additional_track.spotify_id = data['spotify_id']
            if 'covert_art_url' in data :
                new_additional_track.covert_art_url = data['covert_art_url']

            for genre_id in data["genres"]:
                if (ge := GenreModel.query.filter_by(genre_id=genre_id).first()):
                    new_additional_track.genres.append(ge)
                else:
                    return err_resp("Genre %s not found!" % genre_id, 404)

            db.session.add(new_additional_track)
            db.session.commit()

            resp = message(True, "Track have been added to validation.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()