"""API Endpoints for users."""
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse

import exceptions
import public
import serializers


class TodoResource(Resource):
    """API Endpoint to manage TODO."""

    todo_list_parser = reqparse.RequestParser()
    todo_list_parser.add_argument(
        "name", help="This field cannot be blank", required=True
    )

    @jwt_required
    def get(self, id=None):
        """Method to handle get todos request."""
        user = get_jwt_identity()
        if id:
            todo = public.get_todo_by_id(id)
            if not todo:
                raise exceptions.InvalidTodoID(
                    "Todo with ID {} doesn't exists".format(id)
                )
            return serializers.todo_schema.dump(todo)
        else:
            todos = public.get_all_todos_for_user(user)
        return serializers.todos_schema.dump(todos)

    @jwt_required
    def post(self, id=None):
        """Create a new todo."""
        data = self.todo_list_parser.parse_args()
        user = get_jwt_identity()
        public.create_todo_for_user(data["name"], user)
        return {}

    @jwt_required
    def delete(self, id):
        """Delete existing todo."""
        user = get_jwt_identity()
        deleted = public.delete_todo_for_user(id, user)
        return {}
