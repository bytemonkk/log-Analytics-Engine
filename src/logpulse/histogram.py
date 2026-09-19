from dataclasses import dataclass


@dataclass
class StreamingHistogram:
    """Fixed-memory histogram for streaming percentile estimation."""

    min_value: float
    max_value: float
    bucket_count: int

    def __post_init__(self) -> None:
        if self.min_value >= self.max_value:
            raise ValueError("min_value must be less than max_value")

        if self.bucket_count <= 0:
            raise ValueError("bucket_count must be greater than zero")

        self._buckets = [0] * self.bucket_count
        self._count = 0

    @property
    def bucket_width(self) -> float:
        return (self.max_value - self.min_value) / self.bucket_count

    @property
    def count(self) -> int:
        return self._count

    def update(self, value: float) -> None:
        """Add one observation to the histogram."""

        if value < self.min_value:
            index = 0
        elif value >= self.max_value:
            index = self.bucket_count - 1
        else:
            index = int((value - self.min_value) / self.bucket_width)

        self._buckets[index] += 1
        self._count += 1

    def percentile(self, percentile: float) -> float:
        """Estimate a percentile from the histogram."""

        if not 0 <= percentile <= 100:
            raise ValueError("percentile must be between 0 and 100")

        if self._count == 0:
            return 0.0

        target_rank = max(
            1,
            int((percentile / 100) * self._count),
        )

        cumulative = 0

        for index, bucket_count in enumerate(self._buckets):
            cumulative += bucket_count

            if cumulative >= target_rank:
                return self.min_value + index * self.bucket_width

        return self.max_value