from flask import current_app

from src.utils import pagination_resp, internal_err_resp, Paginator
from src.model import TrackModel


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
            track_data = TrackService._load_datas(tracks)

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
    def _load_datas(track_db_obj_list):
        """ Load track's data

        Parameters:
        - List of track db object
        """
        from src.schemas import TrackBase

        track_schema = TrackBase(many=True)

        return track_schema.dump(track_db_obj_list)

    @staticmethod
    def _load_data(track_db_obj):
        """ Load track's data

        Parameters:
        - Track db object
        """
        from src.schemas import TrackBase

        track_schema = TrackBase()

        return track_schema.dump(track_db_obj)
