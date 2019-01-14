"""Models."""
from backend import db, jwt

from passlib.hash import pbkdf2_sha256 as sha256


class UserModel(db.Model):
    """User database table."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @classmethod
    def find_by_username(cls, username):
        """Return user by username."""
        return cls.query.filter_by(username=username).first()

    def save_to_db(self):
        """Use this as auto_commit is False."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        """Generate password hash."""
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        """Verify password hash."""
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    """Model to save revoked tokens."""

    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        """Commit results."""
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """Return True if token is blacklisted."""
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """Util func."""
    jti = decrypted_token["jti"]
    return RevokedTokenModel.is_jti_blacklisted(jti)
