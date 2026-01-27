from app.state import State


def test_update_and_floor(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))
    assert s.snapshot() == {"entries": 0, "tickets": 0, "total": 0}

    s.update("entries", +1)
    assert s.snapshot()["entries"] == 1

    s.update("entries", -5)  # ne doit pas passer sous 0
    assert s.snapshot()["entries"] == 0


def test_reset(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))
    s.update("tickets", +3)
    snap = s.reset()
    assert snap == {"entries": 0, "tickets": 0, "total": 0}
