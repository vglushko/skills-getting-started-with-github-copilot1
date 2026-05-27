import copy
import pytest
from fastapi.testclient import TestClient
from src import app as _app


@pytest.fixture
def client():
    return TestClient(_app.app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(_app.activities)
    yield
    # restore original state
    _app.activities.clear()
    _app.activities.update(original)
