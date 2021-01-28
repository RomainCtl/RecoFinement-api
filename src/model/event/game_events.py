from src import db
from .event import Event, ChangedEvent, DeletionEvent


class GameAddedEvent(Event, db.Model):
    __tablename__ = "game_added_event"

    steamid = db.Column(db.Integer)
    name = db.Column(db.String(255))
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(255))
    website = db.Column(db.String(255))
    developers = db.Column(db.String(255))
    publishers = db.Column(db.String(255))
    price = db.Column(db.String(255))
    recommendations = db.Column(db.Integer)
    release_date = db.Column(db.String(255))


class GameDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", **kwargs)


class GameChangedSteamidEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="steamid", **kwargs)


class GameChangedNameEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="name", **kwargs)


class GameChangedShortDescriptionEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game",
                         attribute_name="short_description", **kwargs)


class GameChangedHeaderImageEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="header_image", **kwargs)


class GameChangedWebsiteEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="website", **kwargs)


class GameChangedDevelopersEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="developers", **kwargs)


class GameChangedPublishersEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="publishers", **kwargs)


class GameChangedPriceEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="price", **kwargs)


class GameChangedRecommendationsEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game",
                         attribute_name="recommendations", **kwargs)


class GameChangedReleaseDateEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="game", attribute_name="release_date", **kwargs)
