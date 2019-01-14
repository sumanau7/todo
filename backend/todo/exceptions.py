"""Models."""
from backend import app
from flask import jsonify


class InvalidTodoID(Exception):
    """API Exceptions."""
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Dict representation."""
        return dict(message=self.message)


@app.errorhandler(InvalidTodoID)
def handle_invalid_usage(error):
    """Func to handle API exceptions and return a generic response."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
