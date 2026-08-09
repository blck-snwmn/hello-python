from pathlib import Path

import pytest

from hello_python.cli import main
from hello_python.models import ReadingStatus
from hello_python.storage import JsonReadingListStore


@pytest.mark.parametrize(
    ("argv", "expected_result"),
    [
        (["add", "Effective Python"], 0),
        (["list"], 0),
        (["finish", "00000000-0000-0000-0000-000000000000"], 1),
    ],
)
def test_every_subcommand_can_be_dispatched(
    tmp_path: Path, argv: list[str], expected_result: int
) -> None:
    path = tmp_path / "reading-list.json"

    assert main(["--file", str(path), *argv]) == expected_result


def test_add_list_and_finish(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "reading-list.json"

    assert main(["--file", str(path), "add", "Effective Python"]) == 0
    item = JsonReadingListStore(path).load()[0]

    assert main(["--file", str(path), "list", "--status", "unread"]) == 0
    assert "Effective Python" in capsys.readouterr().out

    assert main(["--file", str(path), "finish", str(item.id)]) == 0
    assert JsonReadingListStore(path).load()[0].status is ReadingStatus.FINISHED
