from src import db


class SApplicationCategoriesModel(db.Model):
    """
    SApplicationCategories Model for storing application categories
    """
    __tablename__ = "s_application_categories"

    category = db.Column(db.String(45), primary_key=True, index=True)
    count = db.Column(db.Integer)
