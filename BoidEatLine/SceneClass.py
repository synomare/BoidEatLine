from random import choice, uniform
import math
import numpy as np
from scene import *
from BoidClass import Boid

class SwarmScene (Scene):	
    def setup(self):
        self.background_color = 1,1,1
        self.swarm_size = 35
        self.swarm = [Boid(self.size.w, self.size.y, parent=self) for i in range(self.swarm_size)]
        self.location_logger = []
        
    def update(self):		
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
            boid.rotation = math.atan2(*reversed(boid.v)) + math.pi	


                
    def cos_theta_calc(self, boid, b):
        vec_a = b.position - boid.position
        vec_b = boid.v
        vec_a /= abs(vec_a)
        vec_b /= abs(vec_b)
        cos_theta = vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1] / abs(vec_a) * abs(vec_b)
        if 1 < cos_theta:
            cos_theta = 1
        elif cos_theta < -1:
            cos_theta = -1
        return cos_theta
        
    def draw(self):
        stroke(0,0,0)
        stroke_weight(0.3)
        for boid in self.swarm:
            neighbor_set = set([*boid.cohesion_neighbors,*boid.alignment_neighbors,*boid.separation_neighbors])
            for i in neighbor_set:
                if boid.drawing_coordinates and i.drawing_coordinates:
                    line(boid.position[0], boid.position[1], i.position[0], i.position[1])
                
        stroke_weight(1)
        if self.location_logger:
            for i in range(len(self.location_logger) - 1):
                if self.location_logger[i] == None or self.location_logger[i+1] == None:
                    continue
                else:
                    line(self.location_logger[i].x,self.location_logger[i].y,self.location_logger[i+1].x,self.location_logger[i+1].y)

    def touch_began(self,touch):
        self.location_logger.append(touch.location)
        self.touch_detect(touch.location)
    
    def touch_moved(self,touch):
        self.location_logger.append(touch.location)
        self.touch_detect(touch.location)
    
    def touch_ended(self,touch):
        self.location_logger.append(None)
        
    def touch_detect(self,touch_location):
        for i in self.swarm:
            if abs(touch_location - i.position) < 100:
                i.v += (i.position - touch_location) /abs(i.position - touch_location) * 5

    def did_change_size(self):
        for b in self.swarm:
            b.max_x = self.size.w
            b.max_y = self.size.h
                
    def born(self):
        self.swarm.append(Boid(self.size.w, self.size.y, parent=self))

    def kill(self,boid):
        self.swarm.remove(boid)
        boid.remove_from_parent()
        
