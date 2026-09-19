from logpulse.generator import generate_event, generate_events
from logpulse.models import LogEvent


def test_generate_event():
    event = generate_event()

    assert isinstance(event, LogEvent)
    assert event.status_code in {200, 201, 400, 404, 500}
    assert event.latency_ms >= 0
    assert event.response_bytes >= 0


def test_generate_events_is_lazy():
    events = generate_events(100)

    assert not isinstance(events, list)

    generated = list(events)

    assert len(generated) == 100
    assert all(isinstance(event, LogEvent) for event in generated)