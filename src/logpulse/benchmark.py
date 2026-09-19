import time
from pathlib import Path

from logpulse.analytics import analyze
from logpulse.reader import read_jsonl
from logpulse.writer import write_jsonl


def benchmark_generation(count: int, output: Path) -> None:
    start = time.perf_counter()

    write_jsonl(output, count)

    elapsed = time.perf_counter() - start
    size_mb = output.stat().st_size / (1024 * 1024)
    events_per_second = count / elapsed
    mb_per_second = size_mb / elapsed

    print(f"Events: {count:,}")
    print(f"Time: {elapsed:.2f}s")
    print(f"File size: {size_mb:.2f} MB")
    print(f"Events/sec: {events_per_second:,.0f}")
    print(f"Throughput: {mb_per_second:.2f} MB/s")


def benchmark_reading(path: Path) -> None:
    start = time.perf_counter()

    count = 0

    for _ in read_jsonl(path):
        count += 1

    elapsed = time.perf_counter() - start
    size_mb = path.stat().st_size / (1024 * 1024)
    events_per_second = count / elapsed
    mb_per_second = size_mb / elapsed

    print(f"Events: {count:,}")
    print(f"Time: {elapsed:.2f}s")
    print(f"File size: {size_mb:.2f} MB")
    print(f"Events/sec: {events_per_second:,.0f}")
    print(f"Throughput: {mb_per_second:.2f} MB/s")

def benchmark_analysis(path: Path) -> None:
    start = time.perf_counter()

    stats = analyze(read_jsonl(path))

    elapsed = time.perf_counter() - start
    size_mb = path.stat().st_size / (1024 * 1024)

    print(f"Events: {stats.total_requests:,}")
    print(f"Time: {elapsed:.2f}s")
    print(f"File size: {size_mb:.2f} MB")
    print(f"Average latency: {stats.average_latency_ms:.2f} ms")
    print(f"Min latency: {stats.min_latency_ms:.2f} ms")
    print(f"Max latency: {stats.max_latency_ms:.2f} ms")
    print(f"Error rate: {stats.error_rate:.2%}")
    print(f"Total response bytes: {stats.total_response_bytes:,}")
    print(f"P50 latency: {stats.p50_latency_ms:.2f} ms")
    print(f"P95 latency: {stats.p95_latency_ms:.2f} ms")
    print(f"P99 latency: {stats.p99_latency_ms:.2f} ms")