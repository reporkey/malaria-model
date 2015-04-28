class World():
    
    def __init__(self):
        self.environment = None        
        self.agents = []
        
        self.comm_messages = []
        
        # World Size
        self.x_range = [0, 1000]
        self.y_range = [0, 1]
        self.z_range = [0, 1]
        
    def add_agent(self, agent):
        self.agents.append(agent)
    
    # Agents behaviour:
    #   - Observe Environment 
    #   - Send out Communication
    #   - Receive Communication and Perform Action
    def update(self):
        if(self.environment):
            self.environment.update()
        
        # First let the agent observe the current world.
        #   - While observing, agent should create a plan on what it wants to do
        for agent in self.agents:
            agent.observe(self)
            
        # Collect all communication messages
        #   - A comm_message can contain information on what the agent is planning to do.
        self.comm_messages = []
        for agent in self.agents:
            comm_message = agent.communicate()
            if(comm_message):
                self.comm_messages.append( comm_message )
        
        # Perform the (planned) action
        #   - Action can be influenced based comm_message (e.g. planned action might cause collision)
        for agent in self.agents:
            agent.update(self)