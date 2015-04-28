from abmpython.app import App
from abmpython.agent.simple_agent import SimpleAgent

# Create a simple world/system with 10 SimpleAgents
abm = App()
for i in range(0, 10):
    abm.world.add_agent(SimpleAgent())
abm.start()