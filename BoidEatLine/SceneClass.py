from random import choice, uniform
import math
import numpy as np
import pygame
from pygame.math import Vector2
from BoidClass import Boid


class Size:
    def __init__(self, w, h):
        self.w = w
        self.h = h

class SwarmScene:
    def __init__(self, width, height):
        self.size = Size(width, height)
        self.dt = 0
        self.t = 0
        self.setup()

    def setup(self):
        self.background_color = (255, 255, 255)
        self.swarm_size = 35
        self.swarm = [Boid(self.size.w, self.size.h) for _ in range(self.swarm_size)]
        self.location_logger = []
        
    def update(self, dt):
        self.dt = dt
        self.t += dt
        if not any(self.location_logger):
            self.location_logger = []
            
        for boid in self.swarm:
            boid.age += self.dt
            if boid.age >= boid.death_age:
                self.kill(boid)
                self.born()
                for b in self.swarm:
                    if b.drawing_coordinates:
                        for num, y in enumerate(b.drawing_coordinates):
                            self.location_logger.append(y)
                            b.drawing_coordinates.pop(num)
                        self.location_logger.append(None)

            boid.cohesion_neighbors = [b for b in self.swarm if b != boid and abs(b.position - boid.position)<boid.COHESION_DISTANCE and math.degrees(math.acos(self.cos_theta_calc(boid, b))) < boid.COHESION_ANGLE/2]
            boid.separation_neighbors = [b for b in self.swarm if b != boid and abs(b.position - boid.position)<boid.SEPARATION_DISTANCE and math.degrees(math.acos(self.cos_theta_calc(boid, b))) < boid.SEPARATION_ANGLE/2]
            boid.alignment_neighbors = [b for b in self.swarm if b != boid and abs(b.position - boid.position)<boid.ALIGNMENT_DISTANCE and math.degrees(math.acos(self.cos_theta_calc(boid, b))) < boid.ALIGNMENT_ANGLE/2]
            size_of_neighbors = len(set([*boid.cohesion_neighbors,*boid.alignment_neighbors,*boid.separation_neighbors]))
            
            if self.t >5:
                if self.location_logger:
                    for i in self.location_logger:
                        if i != None and abs(boid.position - i) <40:
                            boid.v -= (boid.position - i) * 0.5
                            if abs(boid.position - i) < size_of_neighbors * 3:
                                boid.drawing_coordinates.append \
                                (self.location_logger.pop(self.location_logger.index(i)))
                                
            boid.exe_rule()
            
        for boid in self.swarm:
            boid.position += boid.v
            boid.update_graphics()


                
    def cos_theta_calc(self, boid, b):
        vec_a = b.position - boid.position
        vec_b = boid.v
        vec_a /= abs(vec_a)
        vec_b /= abs(vec_b)
        cos_theta = (vec_a.x * vec_b.x + vec_a.y * vec_b.y) / (abs(vec_a) * abs(vec_b))
        if 1 < cos_theta:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1
        return cos_theta
        
    def draw(self, surface):
        surface.fill(self.background_color)
        for boid in self.swarm:
            neighbor_set = set([*boid.cohesion_neighbors, *boid.alignment_neighbors, *boid.separation_neighbors])
            for i in neighbor_set:
                if boid.drawing_coordinates and i.drawing_coordinates:
                    pygame.draw.line(surface, (0, 0, 0), boid.position, i.position, 1)

        if self.location_logger:
            for i in range(len(self.location_logger) - 1):
                if self.location_logger[i] is None or self.location_logger[i+1] is None:
                    continue
                pygame.draw.line(surface, (0, 0, 0), self.location_logger[i], self.location_logger[i+1], 1)

        for boid in self.swarm:
            surface.blit(boid.image, boid.rect)

    def touch_began(self, pos):
        p = Vector2(pos)
        self.location_logger.append(p)
        self.touch_detect(p)
    
    def touch_moved(self, pos):
        p = Vector2(pos)
        self.location_logger.append(p)
        self.touch_detect(p)
    
    def touch_ended(self, pos=None):
        self.location_logger.append(None)
        
    def touch_detect(self, touch_location):
        for i in self.swarm:
            if abs(touch_location - i.position) < 100:
                i.v += (i.position - touch_location) / abs(i.position - touch_location) * 5

    def did_change_size(self, width, height):
        self.size.w = width
        self.size.h = height
        for b in self.swarm:
            b.max_x = width
            b.max_y = height
                
    def born(self):
        self.swarm.append(Boid(self.size.w, self.size.h))

    def kill(self, boid):
        self.swarm.remove(boid)
        
