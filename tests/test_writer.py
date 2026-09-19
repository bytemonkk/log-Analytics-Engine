from pathlib import Path

from logpulse.writer import write_jsonl


def test_write_jsonl(tmp_path: Path):
    output = tmp_path / "logs.jsonl"

    write_jsonl(output, 10)

    assert output.exists()

    lines = output.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 10