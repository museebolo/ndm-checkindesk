import importlib
import os

from fastapi.testclient import TestClient


def make_client(tmp_path):
    # DATA_PATH must be defined before importing/reloading main,
    # because State(DATA_PATH) is created at import time.
    os.environ["DATA_PATH"] = str(tmp_path / "state.json")

    import app.main

    importlib.reload(app.main)

    return TestClient(app.main.app), app.main


def test_healthz(tmp_path):
    client, _ = make_client(tmp_path)

    r = client.get("/healthz")

    assert r.status_code == 200
    assert r.text == "ok"


def test_update_child_entry(tmp_path):
    client, _ = make_client(tmp_path)

    r = client.post(
        "/update",
        data={
            "key": "children_entries",
            "delta": "+1",
        },
    )

    assert r.status_code == 200
    assert r.json() == {
        "children_entries": 1,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 1,
    }


def test_update_adult_entry(tmp_path):
    client, _ = make_client(tmp_path)

    r = client.post(
        "/update",
        data={
            "key": "adult_entries",
            "delta": "+1",
        },
    )

    assert r.status_code == 200
    assert r.json() == {
        "children_entries": 0,
        "adult_entries": 1,
        "adult_tickets_sold": 0,
        "total_entries": 1,
    }


def test_update_entries_total(tmp_path):
    client, _ = make_client(tmp_path)

    client.post(
        "/update",
        data={
            "key": "children_entries",
            "delta": "+1",
        },
    )

    r = client.post(
        "/update",
        data={
            "key": "adult_entries",
            "delta": "+1",
        },
    )

    assert r.status_code == 200
    assert r.json() == {
        "children_entries": 1,
        "adult_entries": 1,
        "adult_tickets_sold": 0,
        "total_entries": 2,
    }


def test_update_bad_delta(tmp_path):
    client, _ = make_client(tmp_path)

    r = client.post(
        "/update",
        data={
            "key": "adult_entries",
            "delta": "+2",
        },
    )

    assert r.status_code == 400


def test_update_bad_key(tmp_path):
    client, _ = make_client(tmp_path)

    r = client.post(
        "/update",
        data={
            "key": "nope",
            "delta": "+1",
        },
    )

    assert r.status_code == 400


def test_ticket_sale_disabled(tmp_path):
    client, main = make_client(tmp_path)

    main.TICKET_SALES_ENABLED = False

    r = client.post(
        "/sell-adult-ticket",
        data={"delta": "+1"},
    )

    assert r.status_code == 403
    assert r.json()["detail"] == "ticket sales disabled"


def test_sell_adult_ticket(tmp_path):
    client, main = make_client(tmp_path)

    main.TICKET_SALES_ENABLED = True

    r = client.post(
        "/sell-adult-ticket",
        data={"delta": "+1"},
    )

    assert r.status_code == 200
    assert r.json() == {
        "children_entries": 0,
        "adult_entries": 1,
        "adult_tickets_sold": 1,
        "total_entries": 1,
    }


def test_cancel_adult_ticket(tmp_path):
    client, main = make_client(tmp_path)

    main.TICKET_SALES_ENABLED = True

    client.post(
        "/sell-adult-ticket",
        data={"delta": "+1"},
    )

    r = client.post(
        "/sell-adult-ticket",
        data={"delta": "-1"},
    )

    assert r.status_code == 200
    assert r.json() == {
        "children_entries": 0,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 0,
    }


def test_sell_adult_ticket_bad_delta(tmp_path):
    client, main = make_client(tmp_path)

    main.TICKET_SALES_ENABLED = True

    r = client.post(
        "/sell-adult-ticket",
        data={"delta": "+2"},
    )

    assert r.status_code == 400


def test_reset(tmp_path):
    client, main = make_client(tmp_path)

    main.TICKET_SALES_ENABLED = True

    client.post(
        "/update",
        data={
            "key": "children_entries",
            "delta": "+1",
        },
    )

    client.post(
        "/update",
        data={
            "key": "adult_entries",
            "delta": "+1",
        },
    )

    client.post(
        "/sell-adult-ticket",
        data={"delta": "+1"},
    )

    r = client.post("/reset")

    assert r.status_code == 200
    assert r.json() == {
        "children_entries": 0,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 0,
    }
