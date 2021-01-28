from datetime import datetime

from src import db


class Event(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    occured_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    # occured_by = user_id (but not a FK)
    occured_by = db.Column(db.Integer, nullable=False)
    object_id = db.Column(db.Integer, nullable=False)


class ChangedEvent(Event, db.Model):
    __tablename__ = "changed_event"

    model_name = db.Column(db.String, nullable=False)
    attribute_name = db.Column(db.String, nullable=False)
    new_value = db.Column(db.Text, default=None)


class DeletionEvent(Event, db.Model):
    __tablename__ = "deletion_event"

    model_name = db.Column(db.String, nullable=False)
