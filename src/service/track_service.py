from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import TrackModel, MetaUserTrackModel
from src.schemas import TrackBase


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
            track_data = TrackBase.loads(tracks)

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
            db.session.query(TrackModel, func.count(
                MetaUserTrackModel.user_id).label("count")).outerjoin(MetaUserTrackModel).group_by(TrackModel.track_id).order_by(text("count DESC")),
            page,
        )

        try:
            tracks = map(lambda t: t[0], tracks)
            track_data = TrackBase.loads(tracks)

            return pagination_resp(
                message="Most popular track data sent",
                content=track_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
