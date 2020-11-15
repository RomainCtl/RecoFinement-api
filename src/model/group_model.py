from src import db

InvitationModel = db.Table("invitations",
                           db.Column("user_id", db.Integer, db.ForeignKey(
                               "user.user_id", ondelete="CASCADE"), primary_key=True),
                           db.Column("group_id", db.Integer, db.ForeignKey(
                               "group.group_id", ondelete="CASCADE"), primary_key=True)
                           )


class RecommendedApplicationForGroupModel(db.Model):
    """
    RecommendedApplication Model for storing recommended applications for a group
    """
    __tablename__ = "recommended_application_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey(
        "application.app_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class RecommendedBookForGroupModel(db.Model):
    """
    RecommendedBook Model for storing recommended books for a group
    """
    __tablename__ = "recommended_book_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    isbn = db.Column(db.String(13), db.ForeignKey(
        "book.isbn", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class RecommendedGameForGroupModel(db.Model):
    """
    RecommendedGame Model for storing recommended games for a group
    """
    __tablename__ = "recommended_game_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class RecommendedMovieForGroupModel(db.Model):
    """
    RecommendedMovie Model for storing recommended movies for a group
    """
    __tablename__ = "recommended_movie_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey(
        "movie.movie_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class RecommendedSerieForGroupModel(db.Model):
    """
    RecommendedSerie Model for storing recommended series for a group
    """
    __tablename__ = "recommended_serie_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey(
        "serie.serie_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class RecommendedTrackForGroupModel(db.Model):
    """
    RecommendedTrack Model for storing recommended tracks for a group
    """
    __tablename__ = "recommended_track_for_group"

    group_id = db.Column(db.Integer, db.ForeignKey(
        "group.group_id", ondelete="CASCADE"), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey(
        "track.track_id", ondelete="CASCADE"), primary_key=True)
    score = db.Column(db.Float)
    engine = db.Column(db.String)
    engine_priority = db.Column(db.Integer)


class GroupModel(db.Model):
    """
    Group Model for storing group related details
    """
    __tablename__ = "group"

    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id", ondelete="CASCADE"))

    invitations = db.relationship("UserModel", secondary=InvitationModel,
                                  lazy="dynamic", backref=db.backref("invitations", lazy="dynamic", cascade="all,delete"), cascade="all,delete")

    recommended_applications = db.relationship(
        "RecommendedApplicationForGroupModel", lazy="subquery")
    recommended_books = db.relationship(
        "RecommendedBookForGroupModel", lazy="subquery")
    recommended_games = db.relationship(
        "RecommendedGameForGroupModel", lazy="subquery")
    recommended_movies = db.relationship(
        "RecommendedMovieForGroupModel", lazy="subquery")
    recommended_series = db.relationship(
        "RecommendedSerieForGroupModel", lazy="subquery")
    recommended_tracks = db.relationship(
        "RecommendedTrackForGroupModel", lazy="subquery")
