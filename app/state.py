from __future__ import annotations
import json
import os
import tempfile
import threading
from pathlib import Path


class State:
    def __init__(self, data_path: str):
        self.path = Path(data_path)
        self.lock = threading.Lock()
        self.entries = 0
        self.tickets = 0
        self.load()

    def load(self):
        try:
            if self.path.exists():
                with self.path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.entries = int(data.get("entries", 0))
                    self.tickets = int(data.get("tickets", 0))
        except Exception:
            self.entries, self.tickets = 0, 0

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=self.path.name, dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(
                    {"entries": self.entries, "tickets": self.tickets},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
            os.replace(tmp_name, self.path)
        finally:
            try:
                if os.path.exists(tmp_name):
                    os.remove(tmp_name)
            except Exception:
                pass

    def update(self, key: str, delta: int) -> dict:
        with self.lock:
            if key == "entries":
                self.entries = max(0, self.entries + delta)
            elif key == "tickets":
                self.tickets = max(0, self.tickets + delta)
            else:
                raise ValueError("bad key")
            self.save()
            return self.snapshot()

    def reset(self) -> dict:
        with self.lock:
            self.entries, self.tickets = 0, 0
            self.save()
            return self.snapshot()

    def snapshot(self) -> dict:
        return {
            "entries": self.entries,
            "tickets": self.tickets,
            "total": self.entries + self.tickets,
        }
