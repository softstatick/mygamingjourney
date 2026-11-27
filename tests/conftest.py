import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Konfigurasi khusus untuk testing: DB sekali pakai di memori.
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

import pytest

from app import create_app
from models.models import db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client
