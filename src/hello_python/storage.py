from pathlib import Path
from typing import Protocol

from pydantic import TypeAdapter, ValidationError

from hello_python.models import ReadingItem

_reading_items = TypeAdapter(list[ReadingItem])


class StorageError(Exception):
    """Raised when reading-list data cannot be loaded or saved."""


class ReadingListStore(Protocol):
    def load(self) -> list[ReadingItem]: ...

    def save(self, items: list[ReadingItem]) -> None: ...


class JsonReadingListStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[ReadingItem]:
        if not self.path.exists():
            return []

        try:
            return _reading_items.validate_json(self.path.read_bytes())
        except (OSError, ValidationError) as error:
            raise StorageError(f"could not load {self.path}") from error

    def save(self, items: list[ReadingItem]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            data = _reading_items.dump_json(items, indent=2).decode()
            self.path.write_text(f"{data}\n", encoding="utf-8")
        except OSError as error:
            raise StorageError(f"could not save {self.path}") from error
