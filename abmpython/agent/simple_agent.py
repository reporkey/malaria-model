import numpy as np
import random
from random import randint

class SimpleAgent():
    
    def __init__(self):
        self.location = [randint(0,500), 0, 0]
        
    def observe(self, world):
        agents = world.agents
        environment = world.environment
        return
        
    def communicate(self):
        return None
    
    def update(self, world):
        comm_messages = world.comm_messages
        
        velocity = [randint(-5, 5), random.uniform(-0.001,0.001), random.uniform(-0.001,0.001)]
        self.location = np.add(self.location, velocity)
        
        return    