from datetime import UTC, datetime

from logpulse.models import LogEvent


def test_log_event_creation():
    event = LogEvent(
        timestamp=datetime.now(UTC),
        request_id="req_123",
        service="order-service",
        method="GET",
        endpoint="/api/orders",
        status_code=200,
        latency_ms=143,
        response_bytes=8421,
        client_ip="10.0.2.15",
    )

    assert event.status_code == 200
    assert event.endpoint == "/api/orders"
    assert event.latency_ms == 143