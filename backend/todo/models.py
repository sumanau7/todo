from backend import db


class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(256))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def delete_by_id(cls, id):
        deleted = cls.query.filter_by(id=id).delete()
        db.session.commit()
        return deleted
