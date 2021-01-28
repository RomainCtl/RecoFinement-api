from src import db
from .event import Event, ChangedEvent, DeletionEvent


class SerieAddedEvent(Event, db.Model):
    __tablename__ = "serie_added_event"

    imdbid = db.Column(db.String(255))
    title = db.Column(db.String(255))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    writers = db.Column(db.Text)
    directors = db.Column(db.Text)
    actors = db.Column(db.Text)
    cover = db.Column(db.Text)
    plot_outline = db.Column(db.Text)


class SerieDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", **kwargs)


class SerieChangedImdbidEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="imdbid", **kwargs)


class SerieChangedTitleEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="title", **kwargs)


class SerieChangedStartYearEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="start_year", **kwargs)


class SerieChangedEndYearEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="end_year", **kwargs)


class SerieChangedWritersEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="writers", **kwargs)


class SerieChangedDirectorsEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="directors", **kwargs)


class SerieChangedActorsEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="actors", **kwargs)


class SerieChangedCoverEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="cover", **kwargs)


class SerieChangedPlotOutlineEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="serie", attribute_name="plot_outline", **kwargs)
