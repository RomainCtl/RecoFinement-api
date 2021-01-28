from src import db
from .event import Event, ChangedEvent, DeletionEvent


class ApplicationAddedEvent(Event, db.Model):
    __tablename__ = "application_added_event"

    name = db.Column(db.String(255))
    size = db.Column(db.String(255))
    installs = db.Column(db.String(255))
    type = db.Column(db.String(45))
    price = db.Column(db.String(45))
    content_rating = db.Column(db.String(255))
    last_updated = db.Column(db.String(255))
    current_version = db.Column(db.String(255))
    android_version = db.Column(db.String(255))
    cover = db.Column(db.Text)


class ApplicationDeletedEvent(DeletionEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", **kwargs)


class ApplicationChangedNameEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", attribute_name="name", **kwargs)


class ApplicationChangedSizeEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", attribute_name="size", **kwargs)


class ApplicationChangedInstallsEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application",
                         attribute_name="installs", **kwargs)


class ApplicationChangedTypeEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", attribute_name="type", **kwargs)


class ApplicationChangedPriceEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", attribute_name="price", **kwargs)


class ApplicationChangedContentRatingEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application",
                         attribute_name="content_rating", **kwargs)


class ApplicationChangedLastUpdatedEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application",
                         attribute_name="last_updated", **kwargs)


class ApplicationChangedCurrentVersionEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application",
                         attribute_name="current_version", **kwargs)


class ApplicationChangedAndroidVersionEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application",
                         attribute_name="android_version", **kwargs)


class ApplicationChangedCoverEvent(ChangedEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, model_name="application", attribute_name="cover", **kwargs)
