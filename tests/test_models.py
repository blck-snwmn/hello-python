from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from hello_python.models import ReadingItem, ReadingStatus


def test_title_is_trimmed() -> None:
    item = ReadingItem(title="  Effective Python  ")

    assert item.title == "Effective Python"


def test_blank_title_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ReadingItem(title="   ")


def test_finish_returns_a_finished_copy() -> None:
    item = ReadingItem(title="Effective Python")
    finished_at = datetime(2026, 8, 9, tzinfo=UTC)

    finished = item.finish(at=finished_at)

    assert item.status is ReadingStatus.UNREAD
    assert finished.status is ReadingStatus.FINISHED
    assert finished.finished_at == finished_at
