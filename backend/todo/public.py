"""Public interface for TODO."""
import models


def get_todo_by_id(id):
    """Get todo resource by ID."""
    if not id:
        return None
    return models.Todo.get_by_id(id)


def get_all_todos_for_user(user_id):
    """Get all todos for user."""
    return models.Todo.get_by_user_id(user_id)


def create_todo_for_user(name, user_id):
    """Create todo for user."""
    todo_list = models.Todo(name=name, user_id=user_id)
    todo_list.save_to_db()


def delete_todo_for_user(id, user_id):
    """Delete todo for user give a resource ID."""
    todo = models.Todo.get_by_id(id)
    if not todo or todo.user_id != user_id:
        return None
    return models.Todo.delete_by_id(id)
