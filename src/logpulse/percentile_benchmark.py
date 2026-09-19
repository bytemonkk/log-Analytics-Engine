from pathlib import Path

from logpulse.analytics import analyze
from logpulse.histogram import StreamingHistogram
from logpulse.reader import read_jsonl


def benchmark_percentiles(path: Path) -> None:
    events = read_jsonl(path)

    exact_stats = analyze(events)

    histogram = StreamingHistogram(
        min_value=0,
        max_value=1500,
        bucket_count=1500,
    )

    for latency in exact_stats.latencies:
        histogram.update(latency)

    print("Exact percentiles:")
    print(f"P50: {exact_stats.p50_latency_ms:.2f} ms")
    print(f"P95: {exact_stats.p95_latency_ms:.2f} ms")
    print(f"P99: {exact_stats.p99_latency_ms:.2f} ms")

    print("\nHistogram percentiles:")
    print(f"P50: {histogram.percentile(50):.2f} ms")
    print(f"P95: {histogram.percentile(95):.2f} ms")
    print(f"P99: {histogram.percentile(99):.2f} ms")

    print("\nAbsolute error:")
    print(
        f"P50: "
        f"{abs(exact_stats.p50_latency_ms - histogram.percentile(50)):.2f} ms"
    )
    print(
        f"P95: "
        f"{abs(exact_stats.p95_latency_ms - histogram.percentile(95)):.2f} ms"
    )
    print(
        f"P99: "
        f"{abs(exact_stats.p99_latency_ms - histogram.percentile(99)):.2f} ms"
    )


if __name__ == "__main__":
    benchmark_percentiles(
        Path("data/raw/test.jsonl"),
    )