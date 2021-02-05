from src.addons import socketio
from src.utils import ws_jwt_required


@socketio.on("/")
@ws_jwt_required
def my_func(message, current_user):
    pass
