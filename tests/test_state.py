from app.state import State


def test_initial_state(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 0,
    }


def test_children_entries(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.update("children_entries", +1)

    assert s.snapshot() == {
        "children_entries": 1,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 1,
    }


def test_adult_entries(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.update("adult_entries", +1)

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 1,
        "adult_tickets_sold": 0,
        "total_entries": 1,
    }


def test_entries_total(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.update("children_entries", +2)
    s.update("adult_entries", +3)

    assert s.snapshot() == {
        "children_entries": 2,
        "adult_entries": 3,
        "adult_tickets_sold": 0,
        "total_entries": 5,
    }


def test_entries_cannot_be_negative(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.update("children_entries", -5)
    s.update("adult_entries", -5)

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 0,
    }


def test_sell_adult_ticket(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.sell_adult_ticket()

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 1,
        "adult_tickets_sold": 1,
        "total_entries": 1,
    }


def test_sell_multiple_adult_tickets(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.sell_adult_ticket()
    s.sell_adult_ticket()
    s.sell_adult_ticket()

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 3,
        "adult_tickets_sold": 3,
        "total_entries": 3,
    }


def test_cancel_adult_ticket(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.sell_adult_ticket()
    s.sell_adult_ticket()
    s.sell_adult_ticket(-1)

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 1,
        "adult_tickets_sold": 1,
        "total_entries": 1,
    }


def test_cancel_adult_ticket_at_zero(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.sell_adult_ticket(-1)

    assert s.snapshot() == {
        "children_entries": 0,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 0,
    }


def test_complete_scenario(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    # 2 children enter.
    s.update("children_entries", +2)

    # 3 adults arrive with tickets bought elsewhere.
    s.update("adult_entries", +3)

    # 4 adults buy their tickets here.
    for _ in range(4):
        s.sell_adult_ticket()

    assert s.snapshot() == {
        "children_entries": 2,
        "adult_entries": 7,
        "adult_tickets_sold": 4,
        "total_entries": 9,
    }


def test_state_is_persistent(tmp_path):
    p = tmp_path / "state.json"

    s = State(str(p))
    s.update("children_entries", +2)
    s.update("adult_entries", +3)
    s.sell_adult_ticket()

    # Simulate application restart.
    s = State(str(p))

    assert s.snapshot() == {
        "children_entries": 2,
        "adult_entries": 4,
        "adult_tickets_sold": 1,
        "total_entries": 6,
    }


def test_reset(tmp_path):
    p = tmp_path / "state.json"
    s = State(str(p))

    s.update("children_entries", +2)
    s.update("adult_entries", +3)
    s.sell_adult_ticket()

    snap = s.reset()

    assert snap == {
        "children_entries": 0,
        "adult_entries": 0,
        "adult_tickets_sold": 0,
        "total_entries": 0,
    }
