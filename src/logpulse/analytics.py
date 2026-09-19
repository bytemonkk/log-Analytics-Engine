from dataclasses import dataclass, field

from logpulse.histogram import StreamingHistogram
from logpulse.models import LogEvent


@dataclass
class LogStats:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_latency_ms: float = 0.0
    min_latency_ms: float = float("inf")
    max_latency_ms: float = 0.0
    total_response_bytes: int = 0

    histogram: StreamingHistogram = field(
        default_factory=lambda: StreamingHistogram(
            min_value=0,
            max_value=1500,
            bucket_count=1500,
        )
    )

    def update(self, event: LogEvent) -> None:
        self.total_requests += 1

        if event.status_code < 400:
            self.successful_requests += 1
        else:
            self.failed_requests += 1

        self.total_latency_ms += event.latency_ms
        self.min_latency_ms = min(
            self.min_latency_ms,
            event.latency_ms,
        )
        self.max_latency_ms = max(
            self.max_latency_ms,
            event.latency_ms,
        )
        self.total_response_bytes += event.response_bytes

        self.histogram.update(event.latency_ms)

    @property
    def average_latency_ms(self) -> float:
        if self.total_requests == 0:
            return 0.0

        return self.total_latency_ms / self.total_requests

    @property
    def error_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0

        return self.failed_requests / self.total_requests

    @property
    def p50_latency_ms(self) -> float:
        return self.histogram.percentile(50)

    @property
    def p95_latency_ms(self) -> float:
        return self.histogram.percentile(95)

    @property
    def p99_latency_ms(self) -> float:
        return self.histogram.percentile(99)


def analyze(events):
    stats = LogStats()

    for event in events:
        stats.update(event)

    return stats