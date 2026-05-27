import urllib.parse

from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    email = "testuser@example.com"
    activity = "Chess Club"
    path = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    r = client.post(path)
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate():
    email = "dup@example.com"
    activity = "Programming Class"
    path = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    r1 = client.post(path)
    assert r1.status_code == 200
    r2 = client.post(path)
    assert r2.status_code == 400


def test_remove_participant_success():
    email = "remove_me@example.com"
    activity = "Gym Class"
    signup_path = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    r = client.post(signup_path)
    assert r.status_code == 200

    delete_path = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    r2 = client.delete(delete_path)
    assert r2.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_remove_nonexistent():
    activity = "Gym Class"
    delete_path = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote('noone@example.com')}"
    r = client.delete(delete_path)
    assert r.status_code == 404
