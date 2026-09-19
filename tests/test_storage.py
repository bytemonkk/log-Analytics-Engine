from pathlib import Path

import pytest

from logpulse.local_storage import LocalObjectStorage


def test_put_and_get(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    storage.put("logs/test.jsonl", b"hello")

    assert storage.exists("logs/test.jsonl")
    assert storage.get("logs/test.jsonl") == b"hello"


def test_nested_objects(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    storage.put("2026/09/19/app.jsonl", b"logs")

    assert storage.get("2026/09/19/app.jsonl") == b"logs"


def test_list_objects(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    storage.put("logs/a.jsonl", b"a")
    storage.put("logs/b.jsonl", b"b")
    storage.put("metrics/c.json", b"c")

    objects = sorted(storage.list())

    assert objects == [
        "logs/a.jsonl",
        "logs/b.jsonl",
        "metrics/c.json",
    ]


def test_list_with_prefix(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    storage.put("logs/a.jsonl", b"a")
    storage.put("logs/b.jsonl", b"b")
    storage.put("metrics/c.json", b"c")

    objects = sorted(storage.list("logs"))

    assert objects == [
        "logs/a.jsonl",
        "logs/b.jsonl",
    ]


def test_delete(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    storage.put("logs/test.jsonl", b"hello")

    storage.delete("logs/test.jsonl")

    assert not storage.exists("logs/test.jsonl")


def test_missing_object(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    with pytest.raises(FileNotFoundError):
        storage.get("missing.jsonl")


def test_path_traversal_is_rejected(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    with pytest.raises(ValueError):
        storage.put("../outside.txt", b"malicious")
        
def test_streaming_write_and_read(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    with storage.open_write("logs/test.jsonl") as file:
        file.write(b"line 1\n")
        file.write(b"line 2\n")

    with storage.open_read("logs/test.jsonl") as file:
        lines = file.readlines()

    assert lines == [b"line 1\n", b"line 2\n"]
    
def test_streaming_read_missing_object(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    with pytest.raises(FileNotFoundError):
        storage.open_read("missing.jsonl")