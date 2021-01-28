from src import db
from .event import Event, ChangedEvent, DeletionEvent


class MovieAddedEvent(Event, db.Model):
    __tablename__ = "movie_added_event"

    title = db.Column(db.String(255))
    language = db.Column(db.String(255))
    actors = db.Column(db.Text)
    year = db.Column(db.String(255))
    producers = db.Column(db.Text)
    director = db.Column(db.Text)
    writer = db.Column(db.Text)
    imdbid = db.Column(db.String(255))
    tmdbid = db.Column(db.String(255))
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)


class MovieDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", **kwargs)


class MovieChangedTitleEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="title", **kwargs)


class MovieChangedLanguageEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="language", **kwargs)


class MovieChangedActorsEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="actors", **kwargs)


class MovieChangedYearEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="year", **kwargs)


class MovieChangedProducersEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="producers", **kwargs)


class MovieChangedDirectorEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="director", **kwargs)


class MovieChangedWriterEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="writer", **kwargs)


class MovieChangedImdbidEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="imdbid", **kwargs)


class MovieChangedTmdbidEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="tmdbid", **kwargs)


class MovieChangedCoverEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="cover", **kwargs)


class MovieChangedPlotOutlineEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="movie", attribute_name="plot_outline", **kwargs)
