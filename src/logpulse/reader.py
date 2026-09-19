from collections.abc import Iterator

from logpulse.models import LogEvent
from logpulse.storage import ObjectStorage


def read_jsonl(
    storage: ObjectStorage,
    key: str,
) -> Iterator[LogEvent]:
    """Read JSONL records incrementally from object storage."""

    with storage.open_read(key) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            yield LogEvent.model_validate_json(line)