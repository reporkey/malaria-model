import time

from world import World
from visualization.plot_3d import Plot3D

class App():
    
    def __init__(self, visualization='3d', update_rate=30.0):
        if(visualization == '3d'):
            self.renderer = Plot3D()
        self.update_rate_ms = 1.0/update_rate
        self.world = World()
        
        self.state = 0
        self.STATE_RUNNING = 0
        self.STATE_PAUSED = 1
        self.STATE_QUITTING = 2
        
    def start(self):
        while self.state == self.STATE_RUNNING:
            self.world.update()
            
            self.renderer.draw(self.world)
            self.renderer.pause(self.update_rate_ms)