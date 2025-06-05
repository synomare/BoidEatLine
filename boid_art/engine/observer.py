from __future__ import annotations

import asyncio
from typing import Dict

import networkx as nx
from pygame.math import Vector2

from .core import EventBus


class MetaCore:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.graph = nx.Graph()
        self.memories: Dict[int, list[Vector2]] = {}
        bus.on("boid.dead")(self._on_death)

    async def _on_death(self, boid):
        self.memories[id(boid)] = boid.mem.flush()
        self.bus.emit("draw.epitaph", boid=boid, path=self.memories[id(boid)])
        await self._recalc()

    async def _recalc(self):
        self.graph.clear()
        for bid, pts in self.memories.items():
            if len(pts) < 2:
                continue
            prev = pts[0]
            for p in pts[1:]:
                self.graph.add_edge(tuple(prev), tuple(p))
                prev = p
        # compute centrality
        if self.graph.number_of_nodes():
            self.centrality = nx.betweenness_centrality(self.graph)
        else:
            self.centrality = {}

    def get_topk(self, k=3):
        return sorted(self.centrality.items(), key=lambda x: x[1], reverse=True)[:k]

    def draw_graph(self, surface):
        import pygame
        for u, v in self.graph.edges():
            pygame.draw.line(surface, (255, 0, 0), u, v, 1)
