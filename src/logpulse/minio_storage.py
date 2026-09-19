from collections.abc import Iterator
from io import BytesIO
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from logpulse.storage import ObjectStorage


class MinioObjectStorage(ObjectStorage):
    """MinIO-backed implementation of ObjectStorage."""

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False,
    ) -> None:
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )

        self.bucket = bucket

        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

    def put(self, key: str, data: bytes) -> None:
        self.client.put_object(
            self.bucket,
            key,
            BytesIO(data),
            length=len(data),
        )

    def get(self, key: str) -> bytes:
        response = self.client.get_object(
            self.bucket,
            key,
        )

        try:
            return response.read()
        finally:
            response.close()
            response.release_conn()

    def open_read(self, key: str) -> BinaryIO:
        """Open an object for streaming reads."""

        return self.client.get_object(
            self.bucket,
            key,
        )

    def open_write(self, key: str) -> BinaryIO:
        """Open a temporary binary stream for writing."""

        raise NotImplementedError(
            "Streaming writes to MinIO will be implemented separately."
        )

    def exists(self, key: str) -> bool:
        try:
            self.client.stat_object(
                self.bucket,
                key,
            )
            return True
        except S3Error as exc:
            if exc.code in {"NoSuchKey", "NoSuchObject", "NoSuchBucket"}:
                return False
            raise

    def delete(self, key: str) -> None:
        self.client.remove_object(
            self.bucket,
            key,
        )

    def list(self, prefix: str = "") -> Iterator[str]:
        objects = self.client.list_objects(
            self.bucket,
            prefix=prefix,
            recursive=True,
        )

        for obj in objects:
            yield obj.object_name