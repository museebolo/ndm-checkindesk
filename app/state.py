from __future__ import annotations

import json
import os
import tempfile
import threading
from pathlib import Path
from typing import ClassVar


class State:
    VALID_KEYS: ClassVar[frozenset[str]] = frozenset(
        {"children_entries", "adult_entries"}
    )

    def __init__(self, data_path: str):
        self.path = Path(data_path)
        self.lock = threading.Lock()

        self.children_entries = 0
        self.adult_entries = 0
        self.adult_tickets_sold = 0
        self._load()

    def _load(self) -> None:
        try:
            if self.path.exists():
                with self.path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                self.children_entries = int(data.get("children_entries", 0))
                self.adult_entries = int(data.get("adult_entries", 0))
                self.adult_tickets_sold = int(data.get("adult_tickets_sold", 0))

        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            self.children_entries = 0
            self.adult_entries = 0
            self.adult_tickets_sold = 0

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "children_entries": self.children_entries,
            "adult_entries": self.adult_entries,
            "adult_tickets_sold": self.adult_tickets_sold,
        }

        fd, tmp_name = tempfile.mkstemp(
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            suffix=".tmp",
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
                f.flush()
                os.fsync(f.fileno())

            os.replace(tmp_name, self.path)

        finally:
            Path(tmp_name).unlink(missing_ok=True)

    def _state(self) -> dict:
        return {
            "children_entries": self.children_entries,
            "adult_entries": self.adult_entries,
            "adult_tickets_sold": self.adult_tickets_sold,
            "total_entries": (self.children_entries + self.adult_entries),
        }

    def get(self) -> dict:
        with self.lock:
            return self._state()

    def update(self, key: str, delta: int) -> dict:
        """Update a simple entry counter."""

        if key not in self.VALID_KEYS:
            raise ValueError(f"Unknown counter: {key}")

        with self.lock:
            value = getattr(self, key)
            value = max(0, value + delta)

            setattr(self, key, value)

            self._save()

            return self._state()

    def sell_adult_ticket(self, delta: int = 1) -> dict:
        """
        Register or cancel an adult ticket sale.

        Selling a ticket also counts as an adult entry.
        """
        if delta not in {-1, 1}:
            raise ValueError("delta must be -1 or 1")

        with self.lock:
            if delta > 0:
                self.adult_tickets_sold += 1
                self.adult_entries += 1
            elif self.adult_tickets_sold > 0:
                self.adult_tickets_sold -= 1
                self.adult_entries = max(0, self.adult_entries - 1)

            self._save()

            return self._state()

    def reset(self) -> dict:
        """Reset all counters to zero."""
        with self.lock:
            self.children_entries = 0
            self.adult_entries = 0
            self.adult_tickets_sold = 0
            self._save()
            return self._state()

    def snapshot(self) -> dict:
        return self.get()
