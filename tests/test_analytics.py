from datetime import UTC, datetime

import pytest

from logpulse.analytics import LogStats
from logpulse.models import LogEvent


def create_event(status_code: int, latency_ms: float) -> LogEvent:
    return LogEvent(
        timestamp=datetime.now(UTC),
        request_id="req_test",
        service="test-service",
        method="GET",
        endpoint="/test",
        status_code=status_code,
        latency_ms=latency_ms,
        response_bytes=1000,
        client_ip="127.0.0.1",
    )


def test_log_stats():
    stats = LogStats()

    stats.update(create_event(200, 100))
    stats.update(create_event(200, 200))
    stats.update(create_event(500, 300))

    assert stats.total_requests == 3
    assert stats.successful_requests == 2
    assert stats.failed_requests == 1
    assert stats.average_latency_ms == 200
    assert stats.min_latency_ms == 100
    assert stats.max_latency_ms == 300
    assert stats.total_response_bytes == 3000
    assert stats.error_rate == 1 / 3


def test_percentiles():
    stats = LogStats()

    for latency in range(1, 101):
        stats.update(create_event(200, latency))

    assert stats.p50_latency_ms == pytest.approx(50)
    assert stats.p95_latency_ms == pytest.approx(95)
    assert stats.p99_latency_ms == pytest.approx(99)


def test_percentile_empty_stats():
    stats = LogStats()

    assert stats.p50_latency_ms == 0.0
    assert stats.p95_latency_ms == 0.0
    assert stats.p99_latency_ms == 0.0


def test_invalid_percentile():
    stats = LogStats()

    stats.update(create_event(200, 100))

    with pytest.raises(ValueError):
        stats.histogram.percentile(-1)

    with pytest.raises(ValueError):
        stats.histogram.percentile(101)