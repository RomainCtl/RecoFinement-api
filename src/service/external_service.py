from src.utils import err_resp, message, internal_err_resp, Spotify, TMDB, GBooks, validation_error
from src.model import UserModel, ExternalModel, TrackModel, MetaUserTrackModel, MovieModel, MetaUserMovieModel, SerieModel,MetaUserSerieModel, BookModel, MetaUserBookModel
from src import db
from flask import current_app, session
from flask_jwt_extended import decode_token

from dateutil.parser import parse


class ExternalService:
    @staticmethod
    def get_spotify_oauth(user_uuid):
        """ Get spotify oauth url """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if ( ExternalModel.query.filter_by(user_id=user.user_id,service_name="Spotify").first()) is None:
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
        if ExternalModel.query.filter_by(user_id=user.user_id, service_name="Spotify").first() is not None:
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
            if not (external := ExternalModel.query.filter_by(user_id=user.user_id, service_name="Spotify").first()):
                return err_resp("External service not found!", 404)
            try:
                token_info = Spotify.refresh_token(external.refresh_token)
                if "access_token" not in token_info.keys():
                    ExternalModel.query.filter_by(user_id=user.user_id, service_name="Spotify").delete()
                    db.session.commit()
                    return err_resp("Spotify service oauth revoked!", 404)
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
                                artist_name=line['artist_name'],
                                title=line['title'],
                                year=line['year'],
                                release=line['release'],
                                spotify_id=line['spotify_id'],
                                covert_art_url=line['cover_art_url']
                            )
                            db.session.add(new_track)
                            db.session.flush()
                        
                db.session.commit()

                for d in data:
                    for line in d:
                        track = TrackModel.query.filter_by(spotify_id=line['spotify_id']).first()
                        if ((meta := MetaUserTrackModel.query.filter_by(track_id=track.track_id).first()) is None):
                            new_meta_user_track = MetaUserTrackModel(
                                user_id=user.user_id,
                                track_id=track.track_id,
                                play_count=1,
                                last_played_date=line['played_at']
                            )
                            db.session.add(new_meta_user_track)
                            db.session.flush()
                        else :
                            if ((line['played_at'] is not None) and ((meta.last_played_date is None) or (line['played_at'] > meta.last_played_date) )) :
                                meta.last_played_date=line['played_at']
                db.session.commit()

            except Exception as error:
                current_app.logger.error(error)
                return internal_err_resp()

    @staticmethod
    def get_tmdb_oauth(user_uuid):
        """ Get TMDB oauth url """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        
        try:
            if (ExternalModel.query.filter_by(user_id=user.user_id,service_name="TMDB").first()) is None:
                resp = message(True, "TMDB oauth url sent")
                resp["tmdb_url"] = TMDB.oauth_url()
            else:
                resp = message(True, "TMDB is already linked")
                resp["tmdb_url"] = 'linked'
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def tmdb_callback(request_token, user_uuid):
        """ Store tmdb access """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        # Check if the email is taken
        if ExternalModel.query.filter_by(user_id=user.user_id,service_name="TMDB").first() is not None:
            return validation_error(False, "tmdb Oauth is already done.")
        try:
            token_info = TMDB.get_tokens(request_token)

            new_external = ExternalModel(
                service_name='TMDB',
                user_id=user.user_id,
                access_token=token_info['session_id'],
            )

            db.session.add(new_external)
            db.session.flush()

            # Commit changes to DB
            db.session.commit()

            resp = message(True, "TMDB token stored")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
        
    @staticmethod
    def get_tmdb_data(user_uuid, app):
        """ Get tmdb data :  """
        with app.app_context():
            if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
                return err_resp("User not found!", 404)
            if not (external := ExternalModel.query.filter_by(user_id=user.user_id,service_name="TMDB").first()):
                return err_resp("External service not found!", 404)
            try:
                token=external.access_token
                account_id = TMDB.get_account_id(token)
                if 'success' in account_id.keys():
                    ExternalModel.query.filter_by(user_id=user.user_id,service_name="TMDB").delete()
                    db.session.commit()
                    return err_resp("TMDB service oauth revoked!", 404)
                data = TMDB.get_created_list(token,account_id)
                movies = []
                movies.append(TMDB.get_favorite_movies(token,account_id))
                movies.append(TMDB.get_rated_movies(token,account_id))
                movies.append(data['movies'])

                series = []
                series.append(TMDB.get_favorite_series(token,account_id))
                series.append(TMDB.get_rated_series(token,account_id))
                series.append(data['series'])
                
                for movie in movies:
                    for line in movie:
                        if (movie_db := MovieModel.query.filter_by(imdbid=line['imdbid']).first()) is None:
                            new_movie = MovieModel(
                                title = line['title'],
                                language = line['language'],
                                actors = line['actors'],
                                year = line['year'],
                                producers = line['producers'],
                                director = line['director'],
                                writer = line['writer'],
                                imdbid = line['imdbid'],
                                tmdbid = line['tmdbid'],
                                rating = line['rating'],
                                rating_count = line['rating_count'],
                                cover = line['cover']
                            )
                            db.session.add(new_movie)
                            db.session.flush()
                        else :
                            if line['rating'] != movie_db.rating:
                                movie_db.rating = line['rating']
                            if line['rating_count'] != movie_db.rating_count :
                                movie_db.rating_count = line['rating_count']
                db.session.commit()

                for movie in movies:
                    for line in movie:
                        ext_movie = MovieModel.query.filter_by(imdbid=line['imdbid']).first()
                        if ((meta := MetaUserMovieModel.query.filter_by(movie_id=ext_movie.movie_id).first()) is None):
                            new_meta_user_track = MetaUserMovieModel(
                                user_id=user.user_id,
                                movie_id=ext_movie.movie_id,
                                rating = line['user_rating'] if "user_rating" in line.keys() else None,
                                watch_count=1,
                                review_see_count = 1
                            )
                            db.session.add(new_meta_user_track)
                            db.session.flush()
                        else :
                            if line['rating'] != meta.rating:
                                meta.rating = line['rating']
                db.session.commit()

                for serie in series:
                    for line in serie:
                        if (s := SerieModel.query.filter_by(title=line['title'],start_year=line['start_year']).first()) is None:
                            new_serie = SerieModel(
                                title = line['title'],
                                # ! pas present das DB language = line['language'],
                                actors = line['actors'],
                                start_year = line['start_year'],
                                end_year = line['end_year'],
                                directors = line['directors'],
                                writers = line['writers'],
                                rating = line['rating'],
                                rating_count = line['rating_count'],
                                cover = line['cover']
                            )
                            db.session.add(new_serie)
                            db.session.flush()
                        else:
                            if line['rating'] != s.rating:
                                s.rating = line['rating']
                            if line['rating_count'] != s.rating_count:
                                s.rating_count = line['rating_count']
                db.session.commit()
                for serie in series:
                    for line in serie:
                        serie = SerieModel.query.filter_by(title=line['title'],start_year=line['start_year']).first()
                        if ((serie_db := MetaUserSerieModel.query.filter_by(serie_id=serie.serie_id).first()) is None):
                            new_meta_user_track = MetaUserSerieModel(
                                user_id=user.user_id,
                                serie_id=serie.serie_id,
                                rating = line['user_rating'] if "user_rating" in line.keys() else None,
                                review_see_count = 1
                            )
                            db.session.add(new_meta_user_track)
                            db.session.flush()
                        else:
                            if line['rating'] != serie_db.rating :
                                serie_db.rating != line['rating']
                db.session.commit()
            except Exception as error:
                current_app.logger.error(error)
                return internal_err_resp()
    
    @staticmethod
    def get_gbooks_oauth(user_uuid):
        """ Get GBooks oauth url """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        
        try:
            if (ExternalModel.query.filter_by(user_id=user.user_id,service_name="GBooks").first()) is None:
                resp = message(True, "GBooks oauth url sent")
                resp["gbooks_url"] = GBooks.oauth_url(user_uuid)
            else:
                resp = message(True, "GBooks is already linked")
                resp["gbooks_url"] = 'linked'
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def gbooks_callback(user_uuid, code, state):
        """ Store gbooks access """
        if decode_token(state)['identity'] != user_uuid:
            return err_resp("CSRF invalid!", 404)
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        # Check if the email is taken
        if ExternalModel.query.filter_by(user_id=user.user_id,service_name="GBooks").first() is not None:
            return validation_error(False, "gbooks Oauth is already done.")
        try:
            token_info = GBooks.get_token(code, state)

            new_external = ExternalModel(
                service_name='GBooks',
                user_id=user.user_id,
                access_token=token_info['token'],
                refresh_token = token_info['refresh_token']
            )

            db.session.add(new_external)
            db.session.flush()

            # Commit changes to DB
            db.session.commit()

            resp = message(True, "GBooks token stored")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_gbooks_data(user_uuid, app):
        """ Get gbooks data :  """
        with app.app_context():
            if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
                return err_resp("User not found!", 404)
            if not (external := ExternalModel.query.filter_by(user_id=user.user_id,service_name="GBooks").first()):
                return err_resp("External service not found!", 404)
            try:
                token=external.access_token
                refresh_token = external.refresh_token

                books = GBooks.get_data(token, refresh_token)
                if books == "revoked":
                    ExternalModel.query.filter_by(user_id=user.user_id,service_name="GBooks").delete()
                    db.session.commit()
                    return err_resp("Google Books service oauth revoked!", 404)
                
                for line in books:
                    if (book_db := BookModel.query.filter_by(isbn=line['isbn']).first()) is None:                        
                        new_book = BookModel(
                            isbn = line['isbn'],
                            title = line['title'],
                            author = line['author'],
                            year_of_publication = line['year_of_publication'],
                            publisher = line['publisher'],
                            image_url_s = line['image_url_s'],
                            image_url_m = line['image_url_m'],
                            image_url_l = line['image_url_l'],
                            rating = line['rating'],
                            rating_count = line['rating_count']
                        )
                        db.session.add(new_book)
                        db.session.flush()
                    else :
                        if line['rating'] != book_db.rating :
                            book_db.rating = line['rating']
                        if line['rating_count'] != book_db.rating_count :
                            book_db.rating_count = line['rating_count']
                db.session.commit()

                for line in books:
                    if ((meta := MetaUserBookModel.query.filter_by(isbn=line['isbn']).first()) is None):
                        new_meta_user_track = MetaUserBookModel(
                            user_id=user.user_id,
                            isbn = line['isbn'],
                            rating = line['user_rating'],
                            purchase = line['purchase']
                        )
                        db.session.add(new_meta_user_track)
                        db.session.flush()
                    else :
                        if line['rating'] != meta.rating :
                            meta.rating = line['rating']
                        if line ['purchase'] != meta.purchase :
                            meta.purchase = line['purchase']
                    db.session.commit()
            except Exception as error:
                current_app.logger.error(error)
                return internal_err_resp()
