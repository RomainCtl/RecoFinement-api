from flask import current_app
from sqlalchemy import func, text
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import SerieModel, MetaUserSerieModel, GenreModel, ContentType, UserModel, RecommendedSerieModel, RecommendedSerieForGroupModel
from src.schemas import SerieBase, SerieItem, GenreBase, MetaUserSerieBase, SerieExtra


class SerieService:
    @staticmethod
    def search_serie_data(search_term, page):
        """ Search serie data by title """
        series, total_pages = Paginator.get_from(
            SerieModel.query.filter(SerieModel.title.ilike(search_term+"%")).union(
                SerieModel.query.filter(SerieModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            serie_data = SerieBase.loads(series)

            return pagination_resp(
                message="Serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_recommended_series(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from user
        for_user_query = db.session.query(RecommendedSerieModel, SerieModel)\
            .select_from(RecommendedSerieModel)\
            .outerjoin(SerieModel, SerieModel.serie_id == RecommendedSerieModel.serie_id)\
            .filter(RecommendedSerieModel.user_id == user.user_id)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        for_group_query = db.session.query(RecommendedSerieForGroupModel, SerieModel)\
            .select_from(RecommendedSerieForGroupModel)\
            .outerjoin(SerieModel, SerieModel.serie_id == RecommendedSerieForGroupModel.serie_id)\
            .filter(RecommendedSerieForGroupModel.group_id.in_(groups_ids))

        # Popularity
        popularity_query = db.session.query(
            null().label("user_id"),
            null().label("serie_id"),
            null().label("score"),
            null().label("engine"),
            null().label("engine_priority"),
            SerieModel
        ).order_by(
            SerieModel.popularity_score.desc().nullslast(),
        ).limit(200)

        series, total_pages = Paginator.get_from(
            for_user_query
            .union(for_group_query)
            .union(popularity_query)
            .order_by(
                RecommendedSerieModel.engine_priority.desc().nullslast(),
                RecommendedSerieModel.score.desc(),
                SerieModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                if row[0] is None:
                    serie = SerieExtra.load(row[1])
                else:
                    serie = SerieExtra.load(row[1])
                    serie["reco_engine"] = row[0].engine
                    serie["reco_score"] = row[0].score
                return serie

            serie_data = list(map(c_load, series))

            return pagination_resp(
                message="Most popular serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_ordered_genre():
        genres = GenreModel.query.filter_by(
            content_type=ContentType.SERIE).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "Serie genres data sent")
            resp["content"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_meta(user_uuid, serie_id):
        """ Get specific 'meta_user_serie' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if not (meta_user_serie := MetaUserSerieModel.query.filter_by(user_id=user.user_id, serie_id=serie_id).first()):
                meta_user_serie = MetaUserSerieModel(
                    serie_id=serie_id, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_serie.review_see_count += 1
            db.session.add(meta_user_serie)
            db.session.commit()

            meta_user_serie_data = MetaUserSerieBase.load(meta_user_serie)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_serie_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, serie_id, data):
        """ Add 'num_watched_episodes' to 'play_count' or/and update 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (serie := SerieModel.query.filter_by(serie_id=serie_id).first()):
            return err_resp("Serie not found!", 404)

        try:
            if not (meta_user_serie := MetaUserSerieModel.query.filter_by(user_id=user.user_id, serie_id=serie_id).first()):
                meta_user_serie = MetaUserSerieModel(
                    serie_id=serie_id, user_id=user.user_id, num_watched_episodes=0)

            if 'rating' in data:
                # Update average rating on object
                serie.rating = serie.rating or 0
                serie.rating_count = serie.rating_count or 0
                count = serie.rating_count + \
                    (1 if meta_user_serie.rating is None else 0)
                serie.rating = (serie.rating * serie.rating_count - (
                    meta_user_serie.rating if meta_user_serie.rating is not None else 0) + data["rating"]) / count
                serie.rating_count = count

                meta_user_serie.rating = data["rating"]
            if 'num_watched_episodes' in data:
                meta_user_serie.num_watched_episodes += data['num_watched_episodes']

            db.session.add(meta_user_serie)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
