import numpy as np
import random
from random import randint

class ComplexAgent():
    
    def __init__(self):
        self.location = [ randint(0,1000), randint(0,1000), randint(0,1000) ]
        self.target = None
        
    def observe(self, world):
        agents = world.agents
        environment = world.environment
        
        # If there is a food, set that as its target
        if(environment):
            for f in environment.food:
                if(not self.target):
                    self.target = f
                    continue
                
                # Always switch to the closest food source
                target_dist = np.linalg.norm(self.location-self.target)                    
                f_dist = np.linalg.norm(self.location-f)
                if(f_dist < target_dist):
                    self.target = f
        
    def communicate(self):
        return None
    
    def update(self, world, delta):
        environment = world.environment        
        comm_messages = world.comm_messages
        
        # Get normalized distance
        if(self.target):
            distance = np.subtract(self.target, self.location)
            euclidean_distance = np.linalg.norm(distance)
            
            if(euclidean_distance > 0):
                # unit distance vector
                norm_distance = distance / np.linalg.norm(distance)
        
                # Derive new location
                movement = norm_distance * 50.0 * delta
                if(np.linalg.norm(movement) > np.linalg.norm(distance)):
                    self.location += distance
                    for f in environment.food:
                        if(np.array_equal(self.target, f)):
                            environment.food.remove(f)
                    self.target = None
                else:
                    self.location = np.add(self.location, norm_distance * 50.0 * delta)
                
                