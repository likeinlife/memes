import pytest
from fastapi import FastAPI

from container import get_container

from .test_container import get_test_container


@pytest.fixture(scope="module", autouse=True)
def app() -> FastAPI:
    from presentation.api.main import app

    app.dependency_overrides[get_container] = get_test_container

    return app


@pytest.fixture(scope="module", autouse=True)
def client(app: FastAPI):
    from fastapi.testclient import TestClient

    return TestClient(app)
