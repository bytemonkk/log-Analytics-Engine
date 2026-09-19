from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import BinaryIO


class ObjectStorage(ABC):
    """Abstract interface for object storage."""

    @abstractmethod
    def put(self, key: str, data: bytes) -> None:
        """Store an object."""
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> bytes:
        """Retrieve an object."""
        raise NotImplementedError

    @abstractmethod
    def open_read(self, key: str) -> BinaryIO:
        """Open an object for streaming reads."""
        raise NotImplementedError

    @abstractmethod
    def open_write(self, key: str) -> BinaryIO:
        """Open an object for streaming writes."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check whether an object exists."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete an object."""
        raise NotImplementedError

    @abstractmethod
    def list(self, prefix: str = "") -> Iterator[str]:
        """List object keys."""
        raise NotImplementedError