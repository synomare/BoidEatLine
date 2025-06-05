from __future__ import annotations

import asyncio
from typing import List

import numpy as np
from pygame.math import Vector2

from ..engine import Boid, EventBus


class SwarmScene:
    def __init__(self, width: int, height: int, bus: EventBus, swarm_size: int = 35, mem_capacity: int = 256):
        self.bus = bus
        self.width = width
        self.height = height
        self.mem_capacity = mem_capacity
        self.swarm: List[Boid] = [Boid(width, height, bus, mem_capacity=mem_capacity) for _ in range(swarm_size)]
        bus.on("draw.epitaph")(self._on_epitaph)
        self.epitaph_paths: List[List[Vector2]] = []

    async def _on_epitaph(self, boid, path):
        self.epitaph_paths.append(path)

    async def update(self, dt: float):
        boids = list(self.swarm)
        for b in boids:
            neighbors = [n for n in boids if n is not b and (n.position - b.position).length() < 50]
            await b.update(dt, neighbors)
        # remove dead boids
        self.swarm = [b for b in self.swarm if b.age < b.death_age]
        while len(self.swarm) < len(boids):
            self.swarm.append(Boid(self.width, self.height, self.bus, mem_capacity=self.mem_capacity))

    def draw_epitaphs(self, surface):
        import pygame

        for path in self.epitaph_paths:
            if len(path) < 2:
                continue
            for i in range(len(path) - 1):
                pygame.draw.line(surface, (0, 0, 0), path[i], path[i + 1], 1)
        self.epitaph_paths.clear()
