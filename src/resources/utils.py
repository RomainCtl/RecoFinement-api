from marshmallow import Schema, ValidationError


class MSchema(Schema):
    def handle_error(self, exc, data, **kwargs):
        """raise our custom exception when (de)serialization fails."""
        errors = []
        for k, m in exc.messages.items():
            errors.append(*m)
        raise ValidationError(message=errors)
