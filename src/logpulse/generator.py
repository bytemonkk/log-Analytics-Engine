import random
import uuid
from collections.abc import Iterator
from datetime import UTC, datetime

from logpulse.models import LogEvent

SERVICES = [
    "user-service",
    "order-service",
    "payment-service",
    "product-service",
]

METHODS = ["GET", "POST", "PUT", "DELETE"]

ENDPOINTS = [
    "/api/users",
    "/api/orders",
    "/api/products",
    "/api/payments",
]


def generate_event() -> LogEvent:
    """Generate one realistic log event."""
    return LogEvent(
        timestamp=datetime.now(UTC),
        request_id=f"req_{uuid.uuid4().hex[:12]}",
        service=random.choice(SERVICES),
        method=random.choice(METHODS),
        endpoint=random.choice(ENDPOINTS),
        status_code=random.choices(
            [200, 201, 400, 404, 500],
            weights=[70, 10, 8, 7, 5],
        )[0],
        latency_ms=round(random.uniform(5, 1500), 2),
        response_bytes=random.randint(200, 100_000),
        client_ip=f"10.0.{random.randint(0, 255)}.{random.randint(1, 254)}",
    )


def generate_events(count: int) -> Iterator[LogEvent]:
    """Generate events lazily without storing them in memory."""
    for _ in range(count):
        yield generate_event()