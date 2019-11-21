import os
import unittest

from flask_migrate import Manager, Migrate
from flask_script import Manager

from api.main import create_app
from api.main.extensions import db

from api import blueprint

# Create the application in development mode.
# We obviously want to change this to 'prod' in deployment.
app = create_app('prod')

# Register main blueprint from api
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """ Runs Unit Tests """
    tests = unittest.TestLoader().discover("zimmerman/test", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


if __name__ == "__main__":
    manager.run()
