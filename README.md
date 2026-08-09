# hello-python

A small reading-list CLI for exploring modern Python development.

It uses:

- Python 3.14 type annotations, `StrEnum`, `Protocol`, and `pathlib.Path`
- Pydantic for runtime validation of JSON data
- uv for Python and dependency management
- Ruff for linting and formatting
- Pyright for static type checking
- pytest for testing

## Setup

```console
uv sync
```

## Usage

Add an item:

```console
uv run hello-python add "Effective Python" --url https://example.com/effective-python
```

List items:

```console
uv run hello-python list
uv run hello-python list --status unread
```

Mark an item as finished:

```console
uv run hello-python finish 01234567-89ab-cdef-0123-456789abcdef
```

Data is stored in `reading-list.json` in the current directory by default. To use a different file, specify `--file` before the subcommand:

```console
uv run hello-python --file /tmp/books.json list
```

## Development

```console
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run pytest
```
