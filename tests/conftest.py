import pytest
from lib.db import db as _db


@pytest.fixture
def app():
    app = create_app(test=True)
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    return _db
