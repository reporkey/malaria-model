from abmpython.app import App
from abmpython.agent.simple_agent import SimpleAgent
from abmpython.agent.complex_agent import ComplexAgent

from abmpython.environment.food_environment import FoodEnvironment

# Initialize the System Object with the type of visualization
# Pick either '2d' or '3d'
abm = App(visualization='2d')

# Define size of the world (value ranges x,y,z)
world_size = [  [0, 1000],
                [0, 1000],
                [0, 1000] ]
abm.create_world(world_size)

# Add an Environment
abm.world.set_environment( FoodEnvironment() )

# Add in Agents
for i in range(0, 10):
    abm.world.add_agent(ComplexAgent())
    
# Start Simulation
abm.start()