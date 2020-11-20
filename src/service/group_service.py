from flask import current_app

from src import db
from src.utils import err_resp, message, internal_err_resp, Paginator, err_resp
from src.model import GroupModel, UserModel
from src.schemas import GroupObject


class GroupService:
    @staticmethod
    def get_group_data(group_id):
        """ Get group's data by id """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)

        try:
            group_data = GroupObject.load(group)

            resp = message(True, "Group data sent")
            resp["group"] = group_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def create_group(group_name, creator_uuid):
        """ Create group object """
        try:
            group = GroupModel(name=group_name)
            if not (user := UserModel.query.filter_by(uuid=creator_uuid).first()):
                return err_resp("User not found!", 404)
            user.owned_groups.append(group)

            db.session.add(user)
            db.session.commit()

            group_data = GroupObject.load(group)

            resp = message(True, "Group data created")
            resp["group"] = group_data
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def invite_user(group_id, new_member_uuid, current_user_uuid):
        """ Invite member to a group """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)

        if str(group.owner.uuid) != current_user_uuid:
            return err_resp("Unable to invite member to a not owned group", 403)

        if not (member := UserModel.query.filter_by(uuid=new_member_uuid).first()):
            return err_resp("Member not found!", 404)

        if group.invitations.filter_by(user_id=member.user_id).scalar() is not None:
            return err_resp("Invitation already sended !", 400)

        if group.members.filter_by(user_id=member.user_id).scalar() is not None:
            return err_resp("User is already a member of this group !", 400)

        if group.owner.user_id == member.user_id:
            return err_resp("You can not invite yourself to your group !", 400)

        try:
            group.invitations.append(member)

            db.session.add(group)
            db.session.commit()

            group_data = GroupObject.load(group)

            resp = message(True, "User invited to group")
            resp["group"] = group_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def accept_invitation(group_id, user_uuid, current_user_uuid):
        """ Accept invitation """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)

        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("Member not found!", 404)
        
        if not ( UserModel.query.filter_by(uuid=current_user_uuid).first()):
            return err_resp("Member not found!", 404)

        if str(user.uuid) != current_user_uuid:
            return err_resp("Unable to accept an invitation that is not intended to you", 403)

        if group.invitations.filter_by(user_id=user.user_id).scalar() is None:
            return err_resp("Invitation not found !", 404)

        try:
            group.invitations.remove(user)
            group.members.append(user)

            db.session.add(group)
            db.session.commit()

            group_data = GroupObject.load(group)

            resp = message(True, "Member add to group")
            resp["group"] = group_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def delete_invitation(group_id, user_uuid, current_user_uuid):
        """ Refuse / delete invitation """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)

        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("Member not found!", 404)

        if not (UserModel.query.filter_by(uuid=current_user_uuid).first()):
            return err_resp("Member not found!", 404)

        if str(user.uuid) != current_user_uuid and str(group.owner.uuid) != current_user_uuid:
            return err_resp("Unable to delete an invitation that is not intended to you if you are not the group owner", 403)

        if group.invitations.filter_by(user_id=user.user_id).scalar() is None:
            return err_resp("Invitation not found !", 404)

        try:
            group.invitations.remove(user)

            db.session.add(group)
            db.session.commit()

            return "", 204
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def leave_group(group_id, current_user_uuid):
        """ Leave group (if current user is the group owner, this group will be deleted) """
        if not (group := GroupModel.query.filter_by(group_id=group_id).first()):
            return err_resp("Group not found!", 404)
        
        if not (UserModel.query.filter_by(uuid=current_user_uuid).first()):
                return err_resp("User not found!", 404)

        try:
            if str(group.owner.uuid) == current_user_uuid:
                group.members = []
                group.invitations = []
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
