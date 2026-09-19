from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO

from logpulse.storage import ObjectStorage


class LocalObjectStorage(ObjectStorage):
    """Filesystem-backed implementation of ObjectStorage."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, key: str) -> Path:
        root = self.root.resolve()
        path = (root / key).resolve()

        if not path.is_relative_to(root):
            raise ValueError("Object key escapes storage root")

        return path

    def put(self, key: str, data: bytes) -> None:
        path = self._resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def get(self, key: str) -> bytes:
        path = self._resolve(key)

        if not path.exists():
            raise FileNotFoundError(key)

        return path.read_bytes()

    def exists(self, key: str) -> bool:
        return self._resolve(key).exists()

    def delete(self, key: str) -> None:
        path = self._resolve(key)

        if not path.exists():
            raise FileNotFoundError(key)

        path.unlink()

    def list(self, prefix: str = "") -> Iterator[str]:
        base = self._resolve(prefix)

        if not base.exists():
            return

        if base.is_file():
            yield base.relative_to(self.root).as_posix()
            return

        for path in base.rglob("*"):
            if path.is_file():
                yield path.relative_to(self.root).as_posix()
    
    def open_read(self, key: str) -> BinaryIO:
        path = self._resolve(key)

        if not path.exists():
            raise FileNotFoundError(key)

        return path.open("rb")


    def open_write(self, key: str) -> BinaryIO:
        path = self._resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)

        return path.open("wb")