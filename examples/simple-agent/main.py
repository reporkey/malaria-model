import numpy as np
import time

# Visualization
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d

class Draw():
    
    def __init__(self):
        plt.ion()
        plt.show()
        fig = plt.figure()
        self.ax = fig.gca(projection='3d')

        self.ax.set_xlim3d(0, 1000)
        self.ax.set_ylim3d(0, 1)
        self.ax.set_zlim3d(0, 1)

        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')             
        
    def draw_plot(self, world):
        y = np.random.random()
        z = np.random.random()
        self.ax.scatter(world, y, z)
        plt.draw()

fps = 30.0
fps_ms = 1.0/fps
engine = Draw()

for i in range(1000):
    engine.draw_plot(i)
    plt.pause(fps_ms)