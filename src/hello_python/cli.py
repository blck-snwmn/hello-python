import argparse
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import cast
from uuid import UUID

from pydantic import ValidationError

from hello_python.models import ReadingItem, ReadingStatus
from hello_python.storage import JsonReadingListStore, ReadingListStore, StorageError


def add_item(store: ReadingListStore, *, title: str, url: str | None) -> ReadingItem:
    item = ReadingItem.model_validate({"title": title, "url": url})
    items = store.load()
    items.append(item)
    store.save(items)
    return item


def list_items(
    store: ReadingListStore, *, status: ReadingStatus | None = None
) -> list[ReadingItem]:
    items = store.load()
    if status is None:
        return items
    return [item for item in items if item.status is status]


def finish_item(store: ReadingListStore, item_id: UUID) -> ReadingItem | None:
    items = store.load()
    for index, item in enumerate(items):
        if item.id == item_id:
            finished = item.finish()
            items[index] = finished
            store.save(items)
            return finished
    return None


def _add_command(args: argparse.Namespace) -> int:
    store = JsonReadingListStore(cast(Path, args.file))
    item = add_item(
        store,
        title=cast(str, args.title),
        url=cast(str | None, args.url),
    )
    print(f"added {item.id}: {item.title}")
    return 0


def _list_command(args: argparse.Namespace) -> int:
    store = JsonReadingListStore(cast(Path, args.file))
    items = list_items(store, status=cast(ReadingStatus | None, args.status))
    for item in items:
        print(f"{item.id}  {item.status.value:8}  {item.title}")
    return 0


def _finish_command(args: argparse.Namespace) -> int:
    store = JsonReadingListStore(cast(Path, args.file))
    item_id = cast(UUID, args.item_id)
    item = finish_item(store, item_id)
    if item is None:
        print(f"item not found: {item_id}")
        return 1
    print(f"finished {item.id}: {item.title}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Keep a small reading list")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path("reading-list.json"),
        help="JSON file used to store the reading list",
    )
    commands = parser.add_subparsers(required=True)

    add_parser = commands.add_parser("add", help="add a reading item")
    add_parser.add_argument("title")
    add_parser.add_argument("--url")
    add_parser.set_defaults(handler=_add_command)

    list_parser = commands.add_parser("list", help="list reading items")
    list_parser.add_argument("--status", type=ReadingStatus, choices=list(ReadingStatus))
    list_parser.set_defaults(handler=_list_command)

    finish_parser = commands.add_parser("finish", help="mark an item as finished")
    finish_parser.add_argument("item_id", type=UUID)
    finish_parser.set_defaults(handler=_finish_command)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    # argparse adds handler dynamically via set_defaults, so Pyright cannot infer its callable type.
    handler = cast(Callable[[argparse.Namespace], int], args.handler)
    try:
        return handler(args)
    except (StorageError, ValidationError) as error:
        print(f"error: {error}")
        return 2


def run() -> None:
    raise SystemExit(main())
