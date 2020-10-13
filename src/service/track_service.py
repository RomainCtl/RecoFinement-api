from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import TrackModel, MetaUserTrackModel, STrackGenresModel
from src.schemas import TrackBase, TrackObject, STrackGenresBase


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
        tracks, total_pages = Paginator.get_from(
            TrackModel.query.order_by(
                TrackModel.rating_count.desc().nullslast(),
                TrackModel.rating.desc().nullslast()
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
        genres = STrackGenresModel.query.order_by(
            STrackGenresModel.count.desc()).all()

        try:
            genres_data = STrackGenresBase.loads(genres)

            resp = message(True, "track genres data sent")
            resp["track_genres"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
