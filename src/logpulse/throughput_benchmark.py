import time

from logpulse.analytics import analyze
from logpulse.generator import generate_events


def benchmark_throughput(count: int) -> None:
    start = time.perf_counter()

    stats = analyze(generate_events(count))

    elapsed = time.perf_counter() - start

    print(f"Events: {count:,}")
    print(f"Time: {elapsed:.2f}s")
    print(f"Events/sec: {count / elapsed:,.0f}")
    print(f"P50: {stats.p50_latency_ms:.2f} ms")
    print(f"P95: {stats.p95_latency_ms:.2f} ms")
    print(f"P99: {stats.p99_latency_ms:.2f} ms")


if __name__ == "__main__":
    benchmark_throughput(1_000_000)