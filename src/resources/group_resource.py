from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.utils import validation_error

from src.service import GroupService
from src.dto import GroupDto
from src.schemas import GroupCreateSchema, GroupAddMemberSchema

api = GroupDto.api
creation_success = GroupDto.creation_success
added_success = GroupDto.added_success

group_create_schema = GroupCreateSchema()
group_add_member_schema = GroupAddMemberSchema()


@api.route("")
class GroupsResource(Resource):
    """ Groups endpoint
    """

    group_creation = GroupDto.group_creation

    @api.doc(
        "Create a group",
        responses={
            201: ("Group data successfully created", creation_success),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(group_creation, validate=True)
    def post(self):
        """ Create group using name and current user """
        user_uuid = get_jwt_identity()

        # Grab the json data
        group_data = request.get_json()

        # Validate data
        if (errors := group_create_schema.validate(group_data)):
            return validation_error(False, errors)

        return GroupService.create_group(group_data["name"], user_uuid)


@api.route("/<int:group_id>")
class GroupResource(Resource):
    """ Group endpoint
    """

    @api.doc(
        "Get a specific group",
        responses={
            201: ("Group data successfully sended", creation_success),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, group_id):
        """ Get a specific group """
        return GroupService.get_group_data(group_id)

    @api.doc(
        "Leave group (if current user is the group owner, this group will be deleted)",
        responses={
            204: ("Successfully leaving"),
            401: ("Authentication required"),
            404: ("Group not found!"),
        }
    )
    @jwt_required
    def delete(self, group_id):
        """ Leave group (if current user is the group owner, this group will be deleted) """
        user_uuid = get_jwt_identity()

        return GroupService.leave_group(group_id, user_uuid)


@api.route("/<int:group_id>/invitations")
class GroupInvitationsResource(Resource):
    """ Group invitations endpoint
    """

    group_add_member = GroupDto.group_add_member

    @api.doc(
        "Invite user to a group",
        responses={
            201: ("Member successfully invited to the group", added_success),
            401: ("Authentication required"),
            403: ("Unable to invite a member to a not owned group!"),
            404: ("Group or Member not found!"),
        }
    )
    @jwt_required
    @api.expect(group_add_member, validate=True)
    def post(self, group_id):
        """ Invite member to a group """
        user_uuid = get_jwt_identity()

        # Grab the json data
        group_data = request.get_json()

        # Validate data
        if (errors := group_add_member_schema.validate(group_data)):
            return validation_error(False, errors)

        return GroupService.invite_user(group_id, group_data["uuid"], user_uuid)


@api.route("/<int:group_id>/invitations/<string:user_uuid>")
class GroupInvitationsUResource(Resource):
    """ Group invitations endpoint
    """

    @api.doc(
        "Accept invitation to a group",
        responses={
            201: ("Member successfully added to the group", added_success),
            401: ("Authentication required"),
            403: ("Unable to accept an invitation that is not intended to you")
            404: ("Group or User or Invitation not found!"),
        }
    )
    @jwt_required
    def put(self, group_id, user_uuid):
        """ Accept invitation to a group """
        current_user_uuid = get_jwt_identity()

        return GroupService.accept_invitation(group_id, user_uuid, current_user_uuid)

    @api.doc(
        "Delete invitation to a group",
        responses={
            201: ("Invitation to the group successfully deleted"),
            401: ("Authentication required"),
            403: ("Unable to delete an invitation that is not intended to you if you are not the group owner")
            404: ("Group or User or Invitation not found!"),
        }
    )
    @jwt_required
    def delete(self, group_id, user_uuid):
        """ Delete invitation to a group """
        current_user_uuid = get_jwt_identity()

        return GroupService.delete_invitation(group_id, user_uuid, current_user_uuid)
