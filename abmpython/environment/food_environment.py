import numpy as np
import random
from random import randint

class FoodEnvironment():
    
    def __init__(self):
        self.food = []
        self.food_interval = 2.0
        self.MAX_FOOD = 5
        
        # Measuring Time
        self.total_delta = 0.0
        
    def update(self, delta):
        self.total_delta += delta
        while(self.total_delta > self.food_interval and len(self.food) <= self.MAX_FOOD):
            self.food.append([ randint(0,1000), randint(0,1000), randint(0,1000) ])
            self.total_delta -= self.food_interval