import numpy as np

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

class Plot3D():
    
    def __init__(self):
        plt.ion()
        plt.show()
        fig = plt.figure()
        self.ax = fig.gca(projection='3d')
    
    def clear(self, world):
        self.ax.clear()
        
        # Setting World Size and labels
        self.ax.set_xlim3d(world.x_range[0], world.x_range[1])
        self.ax.set_ylim3d(world.y_range[0], world.y_range[1])
        self.ax.set_zlim3d(world.z_range[0], world.z_range[1])
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')                
        
    def draw(self, world):
        self.clear(world)
        
        x_values = []
        y_values = []
        z_values = []
        for agent in world.agents:
            [x, y, z] = agent.location
            x_values.append(x)
            y_values.append(y)
            z_values.append(z)
            
        self.ax.scatter(x_values, y_values, z_values)
        plt.draw()
    
    def pause(self, seconds):
        plt.pause(seconds)