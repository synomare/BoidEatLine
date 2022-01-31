from random import uniform, choice, random, randint
import math
import numpy as np
from scene import *

class Boid (SpriteNode):
    def __init__(self, max_x, max_y, *args, **kwargs):
        img = 'IMG_1962.PNG'
        SpriteNode.__init__(self, img, *args, **kwargs)
        
        self.drawing_coordinates = []
        
        self.age = 1
        self.death_age = randint(20, 90)
        self.scale = 0.0025

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
        self.separation_poewr = np.random.normal(0.0008, 0.005, 1)[0]
        self.alighnmen_power = np.random.normal(0.0015, 0.005, 1)[0]
        self.boundary_force = 1

        self.max_x = max_x
        self.max_y = max_y
        
        a = uniform(0, math.pi*2)
        self.position = (uniform(0, max_x), uniform(0, max_y))
        self.v = Vector2(math.cos(a), math.sin(a))
        
        self.cohesion_neighbors = []
        self.separation_neighbors = []
        self.alighnment_neighbors = []
        
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
        self.v += c * self.separation_poewr
    
    def alignment_rule(self):
        if not self.alighnment_neighbors:
            return 
        v = Vector2()
        for n in self.alighnment_neighbors:
            v += n.v
        m = v / len(self.alighnment_neighbors)
        self.v += m * self.alighnmen_power
    
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
