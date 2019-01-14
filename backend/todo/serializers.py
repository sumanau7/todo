"""Serializers for api endpoint response."""
from marshmallow import Schema, fields


class TodoSchema(Schema):
    """Schema to manage TODO resource response."""
    name = fields.Str()
    id = fields.Int()


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
