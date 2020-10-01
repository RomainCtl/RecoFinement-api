from src import ma

from src.model import MetaUserTrackModel


class MetaUserTrackMeta:
    model = MetaUserTrackModel


class MetaUserTrackBase(ma.SQLAlchemyAutoSchema):
    class Meta(MetaUserTrackMeta):
        pass
