import numpy as np

import matplotlib
# Other backends that can potentially be used:
# http://matplotlib.org/faq/usage_faq.html
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

class Plot2D():
    
    def __init__(self, app):
        self.app = app
        
        plt.ion()
        plt.show()
        
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
    
    def clear(self, world):
        self.ax.clear()
        
        # Setting World Size and labels
        self.ax.set_xlim(world.x_range[0], world.x_range[1])
        self.ax.set_ylim(world.y_range[0], world.y_range[1])
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        
    def on_key(self, event):
        if(event.key == 'escape'):
            self.app.state = self.app.STATE_QUITTING
        elif(event.key == ' '):
            if(self.app.state == self.app.STATE_RUNNING):
                self.app.state = self.app.STATE_PAUSED
            elif(self.app.state == self.app.STATE_PAUSED):
                self.app.state = self.app.STATE_RUNNING
            
    def draw(self, world):
        self.clear(world)
        
        x_food = []
        y_food = []
        if(world.environment):
            food = world.environment.food
            for f in food:
                x_food.append(f[0])
                y_food.append(f[1])
        
        x_values = []
        y_values = []
        for agent in world.agents:
            [x, y, _] = agent.location
            x_values.append(x)
            y_values.append(y)
        
        self.ax.scatter(x_values, y_values, color='blue')
        self.ax.scatter(x_food, y_food, color='red')
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()        
    
    ### DEPRECATED ###    
    # use flush_events not pause()
    # http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
    def pause(self, seconds):
        return
        
    def close(self):
        plt.close()