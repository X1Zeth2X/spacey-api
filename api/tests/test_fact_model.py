from uuid import uuid4
from datetime import datetime

from api.main import db
from api.tests.base import BaseTestCase

from api.main.model.user import User
from api.main.model.fact import Fact


class TestFactModel(BaseTestCase):
    def test_create_fact(self):
        """ Test for fact model """

        with self.client:
            # Create test User
            user = User(
                email="email@test.com",
                username="testUser",
                full_name="Test User",
                password="test1234",
                joined_date=datetime.utcnow(),
            )

            db.session.add(user)
            db.session.commit()

            # Create test fact
            public_id = str(uuid4())[:15]
            fact = Fact(
                public_id=public_id,
                author_id=user.id,
                planet="earth",
                title="Blue Planet",
                content="Life!",
            )

            db.session.add(fact)
            db.session.commit()

            self.assertTrue(isinstance(fact, Fact))
