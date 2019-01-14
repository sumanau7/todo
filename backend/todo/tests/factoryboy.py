from backend import db
import factory

from backend.users.tests import factoryboy as users_factory
from backend.todo import models


class TodoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Todo
        sqlalchemy_session = db.session

    user_id = factory.SubFactory(users_factory.UserModelFactory)
    name = factory.Sequence(lambda n: u'name %d' % n)
