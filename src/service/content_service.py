from flask import current_app
from datetime import datetime

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import MetaUserContentModel, ContentModel, UserModel
from src.schemas import MetaUserContentBase


class ContentService:
    @staticmethod
    def get_meta(user_uuid, content_id):
        """ Get specific 'meta_user_content' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (ContentModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Item not found!", 404)

        try:
            if not (meta_user_content := MetaUserContentModel.query.filter_by(user_id=user.user_id, content_id=content_id).first()):
                meta_user_content = MetaUserContentModel(
                    content_id=content_id, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_content.review_see_count += 1
            meta_user_content.last_review_see_date = datetime.now()
            db.session.add(meta_user_content)
            db.session.commit()

            meta_user_content_data = MetaUserContentBase.load(
                meta_user_content)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_content_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, content_id, data):
        """ Update 'additional_count' to 'count' or/and 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (content := ContentModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Item not found!", 404)

        try:
            if not (meta_user_content := MetaUserContentModel.query.filter_by(user_id=user.user_id, content_id=content_id).first()):
                meta_user_content = MetaUserContentModel(
                    content_id=content_id, user_id=user.user_id, count=0)

            if 'rating' in data:
                # Update average rating on object
                content.rating = content.rating or 0
                content.rating_count = content.rating_count or 0
                count = content.rating_count + \
                    (1 if meta_user_content.rating is None else 0)
                content.rating = (content.rating * content.rating_count - (
                    meta_user_content.rating if meta_user_content.rating is not None else 0) + data["rating"]) / count
                content.rating_count = count

                meta_user_content.rating = data["rating"]
                meta_user_content.last_rating_date = datetime.now()
            if 'additional_count' in data:
                meta_user_content.count += data['additional_count']
                meta_user_content.last_count_increment = datetime.now()

            db.session.add(meta_user_content)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
