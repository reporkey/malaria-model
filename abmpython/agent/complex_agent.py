import numpy as np
import random
from random import randint

class ComplexAgent():
    
    def __init__(self):
        self.location = [ randint(0,500), 0, 0 ]
        self.target = [ randint(400,600), randint(400,600), randint(400,600) ]
        
    def observe(self, world):
        agents = world.agents
        environment = world.environment
        return
        
    def communicate(self):
        return None
    
    def update(self, world, delta):
        comm_messages = world.comm_messages
        
        # Get normalized distance
        distance = np.subtract(self.target, self.location)
        distance = distance / np.linalg.norm(distance)
        
        #
        self.location += distance * 50.0 * delta
        
        return