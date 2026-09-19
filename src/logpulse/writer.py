from logpulse.generator import generate_events
from logpulse.storage import ObjectStorage


def write_jsonl(
    storage: ObjectStorage,
    key: str,
    count: int,
) -> None:
    """Generate events and write them incrementally to object storage."""

    with storage.open_write(key) as file:
        for event in generate_events(count):
            file.write(event.model_dump_json().encode("utf-8"))
            file.write(b"\n")