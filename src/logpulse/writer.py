from pathlib import Path

from logpulse.generator import generate_events


def write_jsonl(path: Path, count: int) -> None:
    """Generate events and write them incrementally to a JSONL file."""
    with path.open("w", encoding="utf-8") as file:
        for event in generate_events(count):
            file.write(event.model_dump_json())
            file.write("\n")