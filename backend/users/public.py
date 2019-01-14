"""Public interface for users module."""
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
)
import models


def is_username_available(username):
    """Return True if username is available."""
    return False if models.UserModel.find_by_username(username) else True


def get_user_by_username(username):
    """Get user by username."""
    return models.UserModel.find_by_username(username)


def create_new_user(username, password):
    """Create new user."""
    new_user = models.UserModel(
        username = username,
        password = models.UserModel.generate_hash(password)
    )
    new_user.save_to_db()
    access_token, refresh_token = create_access_and_refresh_token(identity=username)
    return access_token, refresh_token


def create_access_and_refresh_token(identity):
    """Create access and refresh token."""
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    return access_token, refresh_token


def verify_user(entered_password, saved_password):
    """Verify user password."""
    return models.UserModel.verify_hash(entered_password, saved_password)


def revoke_access_token(jti):
    """Revoke given access token."""
    revoked_token = models.RevokedTokenModel(jti=jti)
    revoked_token.add()
