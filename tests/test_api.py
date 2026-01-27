import importlib
import os
from fastapi.testclient import TestClient


def make_client(tmp_path):
    # IMPORTANT: définir DATA_PATH avant d'importer main (car state = State(DATA_PATH) est créé à l'import)
    os.environ["DATA_PATH"] = str(tmp_path / "state.json")
    import app.main

    importlib.reload(app.main)
    return TestClient(app.main.app)


def test_healthz(tmp_path):
    client = make_client(tmp_path)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.text == "ok"


def test_update_ok(tmp_path):
    client = make_client(tmp_path)
    r = client.post("/update", data={"key": "entries", "delta": "+1"})
    assert r.status_code == 200
    assert r.json()["entries"] == 1


def test_update_bad_delta(tmp_path):
    client = make_client(tmp_path)
    r = client.post("/update", data={"key": "entries", "delta": "+2"})
    assert r.status_code == 400


def test_update_bad_key(tmp_path):
    client = make_client(tmp_path)
    r = client.post("/update", data={"key": "nope", "delta": "+1"})
    assert r.status_code == 400


def test_reset(tmp_path):
    client = make_client(tmp_path)
    client.post("/update", data={"key": "tickets", "delta": "+1"})
    r = client.post("/reset")
    assert r.status_code == 200
    assert r.json() == {"entries": 0, "tickets": 0, "total": 0}
