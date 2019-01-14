"""API Endpoints for users."""
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from flask_restful import Resource, reqparse

import exceptions
import public
import serializers


class UserRegistration(Resource):
    """API endpoint to register new user."""

    parser = reqparse.RequestParser()
    parser.add_argument("username", help="This field cannot be blank", required=True)
    parser.add_argument("password", help="This field cannot be blank", required=True)

    def post(self):
        """Create user."""
        data = self.parser.parse_args()
        username_available = public.is_username_available(data["username"])
        if not username_available:
            raise exceptions.InvalidUsername(
                "User with username {} already exists.".format(data["username"])
            )
        access_token, refresh_token = public.create_new_user(data["username"], data["password"])
        return serializers.user_schema.dump(
            {"username": data["username"], "access_token": access_token, "refresh_token": refresh_token}
        )


class UserLogin(Resource):
    """API endpoint to login existing user."""

    parser = reqparse.RequestParser()
    parser.add_argument("username", help="This field cannot be blank", required=True)
    parser.add_argument("password", help="This field cannot be blank", required=True)

    def post(self):
        """Log a user in."""
        data = self.parser.parse_args()
        current_user = public.get_user_by_username(data["username"])
        if not current_user:
            raise exceptions.InvalidUsername(
                "Username {} doesn't exists or password is incorrect".format(data["username"])
            )
        verified = public.verify_user(data["password"], current_user.password)
        if verified:
            access_token, refresh_token = public.create_access_and_refresh_token(data["username"])
            return serializers.user_schema.dump(
                {"username": data["username"], "access_token": access_token, "refresh_token": refresh_token}
            )
        else:
            raise exceptions.InvalidUsername(
                "Username {} doesn't exists or password is incorrect".format(data["username"])
            )


class UserLogoutAccess(Resource):
    """Logs out a user."""

    @jwt_required
    def post(self):
        """Revoke user token on logout."""
        jti = get_raw_jwt()["jti"]
        public.revoke_access_token(jti)
        return {}


class TokenRefresh(Resource):
    """Refresh user token."""

    @jwt_refresh_token_required
    def post(self):
        """Create a new access token."""
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}
