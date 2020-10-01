from marshmallow import Schema, ValidationError


class DTOSchema(Schema):
    def handle_error(self, exc, data, **kwargs):
        """raise our custom exception when (de)serialization fails."""
        errors = []
        for k, m in exc.messages.items():
            errors += [*m]
        raise ValidationError(message=errors)
