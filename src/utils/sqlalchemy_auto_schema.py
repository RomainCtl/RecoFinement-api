from src import ma


class SQLAlchemyAutoSchema(ma.SQLAlchemyAutoSchema):
    @classmethod
    def load(cls, obj):
        return cls().dump(obj)

    @classmethod
    def loads(cls, objs):
        return cls(many=True).dump(objs)
