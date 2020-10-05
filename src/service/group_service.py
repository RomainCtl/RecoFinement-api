from flask import current_app

from src import db
from src.utils import err_resp, message, internal_err_resp, Paginator
from src.model import GroupModel, UserModel


class GroupService:
    @staticmethod
    def create_group(group_name, creator_uuid):
        """ Create group object """
        try:
            group = GroupModel(name=group_name)
            user = UserModel.query.filter_by(uuid=creator_uuid).first()
            user.owned_groups.append(group)

            db.session.add(user)
            db.session.commit()

            group_data = GroupService._load_data(group)

            resp = message(True, "Group data created")
            resp["group"] = group_data
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def add_member(group_id, new_member_uuid, current_user_uuid):
        """ Add member to a group """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)

        if str(group.owner.uuid) != current_user_uuid:
            return err_resp("Unable to invite member to a not owned group", 403)

        if not (member := UserModel.query.filter_by(uuid=new_member_uuid).first()):
            return err_resp("Member not found!", 404)

        if group.invitations.filter_by(user_id=member.user_id).scalar() is not None:
            return err_resp("Invitation already sended !", 400)

        try:
            group.invitations.append(member)
            # group.members.append(member)

            db.session.add(group)
            db.session.commit()

            group_data = GroupService._load_data(group)

            resp = message(True, "Member add to group")
            resp["group"] = group_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def leave_group(group_id, current_user_uuid):
        """ Leave group (if current user is the group owner, this group will be deleted) """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)

        try:
            if str(group.owner.uuid) == current_user_uuid:
                group.members = []
                db.session.delete(group)
            else:
                current_user = UserModel.query.filter_by(
                    uuid=current_user_uuid).first()
                group.members.remove(current_user)

            db.session.commit()

            return "", 204
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def _load_data(group_db_obj):
        """ Load group's data

        Parameters:
        - Group db object
        """
        from src.schemas import GroupObject

        group_schema = GroupObject()

        return group_schema.dump(group_db_obj)
