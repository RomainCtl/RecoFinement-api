from flask import request, current_app
from flask_socketio import Namespace, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_jwt_extended import decode_token
from flask_socketio import ConnectionRefusedError
from uuid import UUID

from src.addons import socketio
from src.model import UserModel
from src.service import ProfileService


class SandboxResource(Namespace):
    def _check_auth(self, token):
        try:
            tk = decode_token(token)
        except Exception as e:
            raise ConnectionRefusedError("Unauthorized!")

        # Check identity
        if not (user := UserModel.query.filter_by(uuid=tk['identity']).first()):
            raise ConnectionRefusedError("User not found!")

        # Check permissions
        # NOTE ws only used in sandbox, that's why we check this permission here
        if "access_sandbox" not in tk['user_claims']['permissions']:
            raise ConnectionRefusedError("Permission missing!")

        return user

    def on_connect(self):
        current_app.logger.info('Client connected %s' % request.sid)
        emit('server_response', {'on': 'connect',
                                 'action': 'connect', 'message': 'Connected'})

    def on_disconnect(self):
        current_app.logger.info('Client disconnected %s' % request.sid)

    def on_join(self, json):
        current_app.logger.info('Join %s' % request.sid)
        current_user = self._check_auth(json["token"])
        room = "user%s" % current_user.uuid
        join_room(room)
        emit('server_response', {
            'on': 'join',
            'action': 'join',
            'message': 'Room successfully joined',
            'user_uuid': str(current_user.uuid),
            'room': room
        }, room=room)

    def on_leave(self, json):
        current_app.logger.info('Leave %s' % request.sid)
        current_user = self._check_auth(json["token"])
        room = "user%s" % current_user.uuid
        leave_room(room)
        emit('server_response', {
            'on': 'leave',
            'action': 'leave',
            'message': 'Room successfully leaved',
            'user_uuid': str(current_user.uuid),
            'room': room
        }, room=room)

    def on_recommend(self, json):
        current_app.logger.info('Recommend %s' % request.sid)
        if "token" not in json or "profile_uuid" not in json:
            emit('server_response', {
                 'on': 'recommend', 'message': "Error 400, data must contain 'token' and 'profile_uuid' attr!"})
        else:
            current_user = self._check_auth(json["token"])
            room = "user%s" % current_user.uuid

            # Check profile uuid
            try:
                profile_uuid = UUID(json["profile_uuid"], version=4)
            except ValueError:
                emit('server_response', {
                    'on': 'recommend', 'message': "Error 400, 'profile_uuid' not valid uuid4!"})
                return

            current_app.logger.info(
                "Launch recommendation for profile %s" % profile_uuid)

            # Join room if needed
            join_room(room)
            emit('server_response', {
                'on': 'recommend',
                'action': 'join',
                'message': 'Room joined',
                'user_uuid': str(current_user.uuid),
                'room': room
            }, room=room)

            data, code = ProfileService.launch_recommendation(
                profile_uuid, current_user)

            if code == 201:
                emit('server_response', {
                    'on': 'recommend',
                    'action': 'launch recommend',
                    'message': '%s, %s' % (code, data["message"])
                }, room=room)
            else:
                emit('server_response', {
                    'on': 'recommend',
                    'action': 'launch recommend',
                    'message': 'Error %s, %s' % (code, data["message"])
                }, room=room)
