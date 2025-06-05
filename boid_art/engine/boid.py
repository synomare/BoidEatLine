from __future__ import annotations

import asyncio
import math
import random
from dataclasses import dataclass, field
from typing import List

import numpy as np
import pygame
from pygame.math import Vector2

from .memory import SubjectiveStream
from .core import EventBus


@dataclass
class Boid:
    max_x: float
    max_y: float
    bus: EventBus
    mem_capacity: int = 256
    position: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    velocity: Vector2 = field(default_factory=lambda: Vector2(0, 0))
    age: float = 0.0
    death_age: float = field(default_factory=lambda: random.randint(20, 90))
    first_max_speed: float = field(default_factory=lambda: float(np.random.normal(4, 0.008, 1)[0]))

    def __post_init__(self):
        a = random.uniform(0, math.pi * 2)
        self.position = Vector2(random.uniform(0, self.max_x), random.uniform(0, self.max_y))
        self.velocity = Vector2(math.cos(a), math.sin(a))
        self.max_speed = self.first_max_speed
        self.min_speed = float(np.random.normal(2, 0.001, 1)[0])
        self.mem = SubjectiveStream(capacity=self.mem_capacity)

    async def update(self, dt: float, neighbors: List["Boid"]):
        self.age += dt
        self.mem.append(self.position)
        if self.age >= self.death_age:
            self.bus.emit("boid.dead", boid=self)
            return
        self._apply_rules(neighbors)
        self.position += self.velocity * dt * 60
        self._update_speed()

    def _apply_rules(self, neighbors: List["Boid"]):
        if not neighbors:
            return
        center = Vector2()
        separation = Vector2()
        align = Vector2()
        for n in neighbors:
            center += n.position
            separation += (self.position - n.position)
            align += n.velocity
        center /= len(neighbors)
        align /= len(neighbors)
        self.velocity += (center - self.position) * 0.0008
        self.velocity += separation * 0.0008
        self.velocity += align * 0.0015

    def _update_speed(self):
        self.max_speed = self.first_max_speed - 1.2 * self.age / self.death_age
        if self.max_speed < self.min_speed:
            self.max_speed = self.min_speed
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        elif speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)
