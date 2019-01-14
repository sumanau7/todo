"""API Serializers."""
from marshmallow import Schema, fields


class UserSchema(Schema):
    """Response schema for User register and login resource."""

    username = fields.Str()
    access_token = fields.Str()
    refresh_token = fields.Str()


user_schema = UserSchema()
