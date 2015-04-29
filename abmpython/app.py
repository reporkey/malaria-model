import time

from world import World

from visualization.plot_3d import Plot3D
from visualization.plot_2d import Plot2D

class App():
    
    def __init__(self, visualization='3d', update_rate=30.0):
        if(visualization == '2d'):
            self.renderer = Plot2D(self)
        elif(visualization == '3d'):
            self.renderer = Plot3D(self)
        self.update_rate_ms = 1.0/update_rate
        self.last_frame_time = time.time()
        self.delta = 0
        
        self.state = 0
        self.STATE_RUNNING = 0
        self.STATE_PAUSED = 1
        self.STATE_QUITTING = 2
        
    def create_world(self, size):
        self.world = World(size)
        
    def start(self):
        while True:
            if(self.state == self.STATE_RUNNING):
                # Compute delta time
                current_time = time.time()
                self.delta += current_time - self.last_frame_time
                self.last_frame_time = current_time
                
                # Update world based on passed time between frames
                while(self.delta >= self.update_rate_ms):
                    self.world.update(self.delta)                    
                    self.delta -= self.update_rate_ms
                
                # Draw the world
                self.renderer.draw(self.world)
                         
            elif(self.state == self.STATE_QUITTING):
                self.renderer.close()
                break