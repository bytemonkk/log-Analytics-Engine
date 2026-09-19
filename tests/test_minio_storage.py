from logpulse.minio_storage import MinioObjectStorage


def create_storage() -> MinioObjectStorage:
    return MinioObjectStorage(
        endpoint="localhost:9000",
        access_key="logpulse",
        secret_key="logpulse-dev-password",
        bucket="logpulse-test",
        secure=False,
    )


def test_put_and_get():
    storage = create_storage()

    key = "tests/test.txt"
    data = b"hello minio"

    storage.put(key, data)

    assert storage.exists(key)
    assert storage.get(key) == data

    storage.delete(key)

    assert not storage.exists(key)


def test_list():
    storage = create_storage()

    storage.put("logs/a.txt", b"a")
    storage.put("logs/b.txt", b"b")

    objects = sorted(storage.list("logs"))

    assert objects == [
        "logs/a.txt",
        "logs/b.txt",
    ]

    storage.delete("logs/a.txt")
    storage.delete("logs/b.txt")