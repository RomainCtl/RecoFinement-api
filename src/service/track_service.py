from flask import current_app

from src.utils import pagination_resp, internal_err_resp, Paginator
from src.model import TrackModel
from src.schemas import TrackBase


class TrackService:
    @staticmethod
    def search_track_data(search_term, page):
        """ Search track data by title """
        tracks, total_pages = Paginator.get_from(
            TrackModel.query.filter(
                TrackModel.title.ilike("%"+search_term+"%")),
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
    def get_track_list_data(page):
        """ Get list of track """
        tracks, total_pages = Paginator.get_from(
            TrackModel.query,
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
