from pathlib import Path

import pytest

from hello_python.models import ReadingItem
from hello_python.storage import JsonReadingListStore, StorageError


def test_json_store_round_trip(tmp_path: Path) -> None:
    store = JsonReadingListStore(tmp_path / "reading-list.json")
    expected = [
        ReadingItem.model_validate({"title": "Effective Python", "url": "https://example.com/book"})
    ]

    store.save(expected)

    assert store.load() == expected


def test_missing_file_is_an_empty_list(tmp_path: Path) -> None:
    store = JsonReadingListStore(tmp_path / "missing.json")

    assert store.load() == []


def test_invalid_json_is_reported(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("not json", encoding="utf-8")

    with pytest.raises(StorageError):
        JsonReadingListStore(path).load()
