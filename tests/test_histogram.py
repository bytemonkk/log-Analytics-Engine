import pytest

from logpulse.histogram import StreamingHistogram


def test_histogram_counts_values():
    histogram = StreamingHistogram(
        min_value=0,
        max_value=100,
        bucket_count=100,
    )

    histogram.update(10)
    histogram.update(20)
    histogram.update(30)

    assert histogram.count == 3


def test_histogram_percentiles():
    histogram = StreamingHistogram(
        min_value=0,
        max_value=100,
        bucket_count=100,
    )

    for value in range(1, 101):
        histogram.update(value)

    assert histogram.percentile(50) == pytest.approx(50)
    assert histogram.percentile(95) == pytest.approx(95)
    assert histogram.percentile(99) == pytest.approx(99)


def test_empty_histogram():
    histogram = StreamingHistogram(
        min_value=0,
        max_value=100,
        bucket_count=100,
    )

    assert histogram.percentile(50) == 0.0


def test_invalid_configuration():
    with pytest.raises(ValueError):
        StreamingHistogram(
            min_value=100,
            max_value=0,
            bucket_count=100,
        )

    with pytest.raises(ValueError):
        StreamingHistogram(
            min_value=0,
            max_value=100,
            bucket_count=0,
        )


def test_invalid_percentile():
    histogram = StreamingHistogram(
        min_value=0,
        max_value=100,
        bucket_count=100,
    )

    with pytest.raises(ValueError):
        histogram.percentile(-1)

    with pytest.raises(ValueError):
        histogram.percentile(101)