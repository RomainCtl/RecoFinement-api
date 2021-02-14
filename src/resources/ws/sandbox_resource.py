from flask import request, current_app
from flask_socketio import Namespace, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_jwt_extended import decode_token
from flask_socketio import ConnectionRefusedError
from uuid import UUID

from src.addons import socketio
from src.model import UserModel
from src.schemas import ProfileBase
from src.service import ProfileService


class SandboxResource(Namespace):
    def is_auth(func):
        def wrapper(*args, **kwargs):
            if not 'token' in request.headers:
                raise ConnectionRefusedError("Token not found !")

            try:
                tk = decode_token(request.headers["token"])
            except Exception as e:
                raise ConnectionRefusedError("Unauthorized!")

            # Check identity
            if not (user := UserModel.query.filter_by(uuid=tk['identity']).first()):
                raise ConnectionRefusedError("User not found!")

            # Check permissions
            # NOTE ws only used in sandbox, that's why we check this permission here
            if "access_sandbox" not in tk['user_claims']['permissions']:
                raise ConnectionRefusedError("Permission missing!")

            return func(*args, connected_user=user, **kwargs)

        return wrapper

    @is_auth
    def on_connect(self, connected_user):
        current_app.logger.info('Client connected %s' % request.sid)
        emit('server_response', {'on': 'connect',
                                 'action': 'connect', 'message': 'Connected'})

    @is_auth
    def on_disconnect(self, connected_user):
        current_app.logger.info('Client disconnected %s' % request.sid)

    @is_auth
    def on_join(self, connected_user):
        current_app.logger.info('Join %s' % request.sid)
        room = "user%s" % connected_user.uuid
        join_room(room)
        emit('server_response', {
            'on': 'join',
            'action': 'join',
            'message': 'Room successfully joined',
            'user_uuid': str(connected_user.uuid),
            'room': room
        }, room=room)

    @is_auth
    def on_leave(self, connected_user):
        current_app.logger.info('Leave %s' % request.sid)
        room = "user%s" % connected_user.uuid
        leave_room(room)
        emit('server_response', {
            'on': 'leave',
            'action': 'leave',
            'message': 'Room successfully leaved',
            'user_uuid': str(connected_user.uuid),
            'room': room
        }, room=room)

    @is_auth
    def on_recommend(self, json, connected_user):
        current_app.logger.info('Recommend %s' % request.sid)
        if "profile_uuid" not in json:
            emit('server_response', {
                 'on': 'recommend', 'message': "Error 400, data must contain 'profile_uuid' attr!"})
        else:
            room = "user%s" % connected_user.uuid

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
                'user_uuid': str(connected_user.uuid),
                'room': room
            }, room=room)

            data, code, profile = ProfileService.launch_recommendation(
                profile_uuid, connected_user)

            if code == 200:
                emit('server_response', {
                    'on': 'recommend',
                    'action': 'recommend',
                    'message': '%s, %s' % (code, data["message"]),
                    'profile': ProfileBase.load(profile)
                }, room=room)
            else:
                emit('server_response', {
                    'on': 'recommend',
                    'action': 'recommend',
                    'message': 'Error %s, %s' % (code, data["message"]),
                    'profile': ProfileBase.load(profile)
                }, room=room)
