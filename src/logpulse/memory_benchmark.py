import tracemalloc
from time import perf_counter

from logpulse.analytics import LogStats
from logpulse.generator import generate_events


def benchmark_memory(count: int) -> None:
    tracemalloc.start()

    stats = LogStats()

    start = perf_counter()

    for event in generate_events(count):
        stats.update(event)

    elapsed = perf_counter() - start

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Events: {count:,}")
    print(f"Time: {elapsed:.2f}s")
    print(f"Events/sec: {count / elapsed:,.0f}")
    print(f"Current memory: {current / (1024 * 1024):.2f} MB")
    print(f"Peak memory: {peak / (1024 * 1024):.2f} MB")
    print(f"P50: {stats.p50_latency_ms:.2f} ms")
    print(f"P95: {stats.p95_latency_ms:.2f} ms")
    print(f"P99: {stats.p99_latency_ms:.2f} ms")


if __name__ == "__main__":
    benchmark_memory(1_000_000)