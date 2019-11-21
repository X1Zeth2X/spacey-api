import pytest

from api.main import create_app

@pytest.fixture
def app(mocker):
    mocker.patch("flask_sqlalchemy.SQLAlchemy.init_app", return_value=True)
    mocker.patch("flask_sqlalchemy.SQLAlchemy.create_all", return_value=True)
    mocker.patch("example.database.get_all", return_value={})
    app = create_app()
    return app