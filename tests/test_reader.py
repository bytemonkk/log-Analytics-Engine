from pathlib import Path

from logpulse.local_storage import LocalObjectStorage
from logpulse.reader import read_jsonl
from logpulse.writer import write_jsonl


def test_read_jsonl(tmp_path: Path):
    storage = LocalObjectStorage(tmp_path)

    write_jsonl(storage, "logs.jsonl", 10)

    events = list(read_jsonl(storage, "logs.jsonl"))

    assert len(events) == 10
    assert events[0].request_id.startswith("req_")