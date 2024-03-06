import pytest
import sys

from ..app import create_app


@pytest.fixture
def app():
    app = create_app("tests")

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
