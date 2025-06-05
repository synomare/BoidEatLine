import asyncio
import pytest

from boid_art.engine import EventBus, Boid, MetaCore


@pytest.mark.asyncio
async def test_metacore_centrality():
    bus = EventBus()
    meta = MetaCore(bus)
    b = Boid(100, 100, bus)
    b.death_age = 0
    await b.update(1.0, [])
    await asyncio.sleep(0.01)
    assert meta.graph.number_of_nodes() >= 1 or not meta.memories


def test_draw_graph_no_nodes(tmp_path):
    import pygame

    pygame.init()
    surface = pygame.Surface((100, 100))
    bus = EventBus()
    meta = MetaCore(bus)
    meta.draw_graph(surface)
    pygame.quit()
