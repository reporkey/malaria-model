
POPULATION_SIZE = 10
INFECTIOUS_RATE = 0.2

TOTAL_TIME = 10

class Agent:
    def __init__(self, is_infected):
        self.is_infected = is_infected

class Population:
    def __init__(self, population_size, infected_size, suspected_size):
        self.population_size = population_size
        self.infected_size = infected_size
        self.suspected_size = suspected_size
        self.recovery_size = 0
        self.population = []

        # init agents
        for i in range(infected_size):
            agent = Agent(is_infected=True)
            self.population.append(agent)
        for i in range(suspected_size):
            agent = Agent(is_infected=False, is_suspected=True)
            self.population.append(agent)

# simulation start
while True:
    if
