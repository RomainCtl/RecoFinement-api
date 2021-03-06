# Validations with Marshmallow
from marshmallow import fields
from marshmallow.validate import Regexp, Length, Email

from src.utils import DTOSchema


class LoginSchema(DTOSchema):
    """ /auth/login [POST]

    Parameters:
    - Email
    - Password (Str)
    """

    email = fields.Email(required=True, validate=[Length(min=5, max=64)])
    password = fields.Str(required=True, validate=[Length(min=8, max=128)])


class RegisterSchema(DTOSchema):
    """ /auth/register [POST]

    Parameters:
    - Email
    - Username (Str)
    - Password (Str)
    """

    email = fields.Email(required=True, validate=[Length(min=5, max=64)])
    username = fields.Str(
        required=True,
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid username!",
            ),
        ],
    )
    password = fields.Str(
        required=True,
        validate=[
            Length(min=8, max=128),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.+\-#_])[A-Za-z\d@$!%*?&.+\-#_]{8,}",
                error="Password must contain at least minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character !"
            ),
        ],
    )


class ResetSchema(DTOSchema):
    """ /auth/login [POST]

    Parameters:
    - Email
    """
    password = fields.Str(
        required=True,
        validate=[
            Length(min=8, max=128),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}",
                error="Password must contain at least minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character !"
            ),
        ],
    )
    reset_password_token = fields.Str(required=True, validate=[Length(min=50)])


class ForgetSchema(DTOSchema):
    """ /auth/login [POST]

    Parameters:
    - Email
    """
    email = fields.Email(required=True, validate=[Length(min=5, max=64)])
