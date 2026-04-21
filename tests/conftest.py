from __future__ import annotations

import os

import pytest

from src.bank_ai.app_factory import create_app
from src.bank_ai.config import TestingConfig


@pytest.fixture()
def app():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app(TestingConfig)
    app.config.update(SECRET_KEY="test-secret")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
