from flask_restx import Namespace, fields

from .base import GroupBaseObj, GroupItemObj, messageObj


class GroupDto:
    api = Namespace("group", description="Group related operations.")

    # Objects
    api.models[GroupBaseObj.name] = GroupBaseObj
    group_base = GroupBaseObj

    api.models[GroupItemObj.name] = GroupItemObj
    group_item = GroupItemObj

    # Responses
    creation_success = api.model(
        "Group Data Response",
        {
            **messageObj,
            "group": fields.Nested(group_base),
        },
    )

    added_success = api.model(
        "Group Item Response",
        {
            **messageObj,
            "group": fields.Nested(group_item),
        }
    )

    # Excepted data
    group_creation = api.model(
        "Group creation data",
        {
            "name": fields.String(required=True)
        }
    )

    group_add_member = api.model(
        "Group add member",
        {
            "uuid": fields.String(required=True)
        }
    )
