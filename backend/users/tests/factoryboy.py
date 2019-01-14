from backend import db
import factory
import factory.alchemy
from backend.users import models


class UserModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.UserModel
        sqlalchemy_session = db.session

    username = factory.Sequence(lambda n: u'username %d' % n)
    password = factory.Sequence(lambda n: u'password %d' % n)
