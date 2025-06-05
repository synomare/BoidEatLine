import asyncio
import pytest

from boid_art.engine import EventBus, Boid


@pytest.mark.asyncio
async def test_boid_death_event():
    bus = EventBus()
    events = []

    @bus.on("draw.epitaph")
    async def on_epitaph(**payload):
        events.append(payload)

    b = Boid(100, 100, bus)
    b.death_age = 0
    await b.update(1.0, [])
    await asyncio.sleep(0.01)
    assert len(events) == 1
