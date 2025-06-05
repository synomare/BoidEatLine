from random import uniform, choice, random, randint
import math
import numpy as np
import pygame
from pygame.math import Vector2

# pygame does not provide a Point class, so Vector2 is used instead
Point = Vector2

class Boid(pygame.sprite.Sprite):
    def __init__(self, max_x, max_y):
        super().__init__()
        # create a simple triangular surface to represent the boid
        self.image_orig = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image_orig, (0, 0, 0), [(10, 0), (0, 20), (20, 20)])
        self.image = self.image_orig
        self.rect = self.image.get_rect(center=(uniform(0, max_x), uniform(0, max_y)))
        
        self.drawing_coordinates = []
        
        self.age = 1
        self.death_age = randint(20, 90)
        self.scale = 1

        self.first_max_speed = np.random.normal(4, 0.008, 1)[0]
        self.max_speed = self.first_max_speed
        self.min_speed= np.random.normal(2, 0.001, 1)[0]

        self.COHESION_DISTANCE = np.random.normal(150, 20, 1)[0]
        self.SEPARATION_DISTANCE = np.random.normal(20, 4, 1)[0]
        self.ALIGNMENT_DISTANCE = np.random.normal(120, 20, 1)[0]

        self.COHESION_ANGLE = np.random.normal(180, 80, 1)[0]
        self.SEPARATION_ANGLE = np.random.normal(180, 90, 1)[0]
        self.ALIGNMENT_ANGLE = np.random.normal(180, 70, 1)[0]
        
        self.cohesion_power = np.random.normal(0.0008, 0.005, 1)[0]
        self.separation_power = np.random.normal(0.0008, 0.005, 1)[0]
        self.alighnment_power = np.random.normal(0.0015, 0.005, 1)[0]
        self.boundary_force = 1

        self.max_x = max_x
        self.max_y = max_y
        
        a = uniform(0, math.pi*2)
        self.position = Vector2(uniform(0, max_x), uniform(0, max_y))
        self.v = Vector2(math.cos(a), math.sin(a))
        self.rect.center = self.position
        self.rotation = 0
        
        self.cohesion_neighbors = []
        self.separation_neighbors = []
        self.alignment_neighbors = []
        
    def exe_rule(self):
        self.cohesion_rule()
        self.separation_rule()
        self.alignment_rule()
        self.boundary_rule()
        self.speed_rule()
        self.age_effect()

    def cohesion_rule(self):
        if not self.cohesion_neighbors:
            return 
        p = Point()
        for n in self.cohesion_neighbors:
            p += n.position
        m = p / len(self.cohesion_neighbors)
        self.v += (m - self.position) * self.cohesion_power
    
    def separation_rule(self):
        if not self.separation_neighbors:
            return 
        c = Vector2()
        for n in self.separation_neighbors:
            c += (self.position - n.position)
        self.v += c * self.separation_power
    
    def alignment_rule(self):
        if not self.alignment_neighbors:
            return 
        v = Vector2()
        for n in self.alignment_neighbors:
            v += n.v
        m = v / len(self.alignment_neighbors)
        self.v += m * self.alighnment_power
    
    def boundary_rule(self):
        v = Vector2()
        if self.position.x < 0:
            v.x = 1
        if self.position.x > self.max_x:
            v.x = -1
        if self.position.y < 0:
            v.y = 1
        if self.position.y > self.max_y:
            v.y = -1
        self.v += v * self.boundary_force
    
    def speed_rule(self):
        if abs(self.v) > self.max_speed:
            self.v *= (self.max_speed / abs(self.v))
        if abs(self.v) < self.min_speed:
            self.v *= (self.min_speed / abs(self.v))
            
    def age_effect(self):
        self.max_speed =  self.first_max_speed - 1.2 * self.age/self.death_age

    def update_graphics(self):
        """Update sprite image orientation and rect position."""
        self.rotation = math.atan2(self.v.y, self.v.x) + math.pi / 2
        angle = -math.degrees(self.rotation)
        self.image = pygame.transform.rotate(self.image_orig, angle)
        self.rect = self.image.get_rect(center=self.position)
