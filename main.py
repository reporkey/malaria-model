from functools import reduce
from enum import *
from random import *
import numpy as np
import matplotlib.pyplot as plt

# N = 100                      # Population size
# SUSCEPTIBLE_SIZE = 95
# INFECTIOUS_SIZE = 5
# IMMUNE_SIZE = 0

# Beta = 0.1                  # Rate at which two specific individuals come into effective contact
# RECOVERY_RATE = 0.2
# IMMUNE_REMOVE_RATE = 0.2
# MAX_CONTACT_NUMBER = 10    # Max number of contacted individual with a single per time unit


# plot setting

# breakout size comparison by vary beta
N = 5000
SUSCEPTIBLE_SIZE = 995
INFECTIOUS_SIZE = 5
IMMUNE_SIZE = 0
MAX_CONTACT_NUMBER = 10
RECOVERY_RATE = 0
IMMUNE_REMOVE_RATE = 0

BETAS = np.linspace(start=0.1, stop=1, num=10)
results = []




class State(Enum):
    SUSCEPTIBLE = auto()
    INFECTIOUS = auto()
    IMMUNE = auto()

class Individual:
    def __init__(self, state: State):
        self.state = state

class Population:
    def __init__(self, individuals=None):
        if individuals is None:
            self.population_size = N
            self.susceptible_size = SUSCEPTIBLE_SIZE
            self.infectious_size = INFECTIOUS_SIZE
            self.immune_size = IMMUNE_SIZE
            self.individuals = []
            self.generate()
        else:
            self.individuals = individuals
            self.update_size()

    # generate individuals
    def generate(self):
        for _ in range(self.susceptible_size):
            self.individuals.append(Individual(state=State.SUSCEPTIBLE))
        for _ in range(self.infectious_size):
            self.individuals.append(Individual(state=State.INFECTIOUS))
        for _ in range(self.immune_size):
            self.individuals.append(Individual(state=State.IMMUNE))

    # filter out individuals in certain state, e.g population.filter(State.IMMUNE) => [immune indi]
    def filter(self, state: State):
        return filter(lambda individual: (individual.state is state), self.individuals)

    def update_size(self):
        self.susceptible_size = len(list(self.filter(State.SUSCEPTIBLE)))
        self.infectious_size = len(list(self.filter(State.INFECTIOUS)))
        self.immune_size = len(list(self.filter(State.IMMUNE)))
        self.population_size = self.susceptible_size + self.infectious_size + self.immune_size


for Beta in BETAS:
    breakout = 0
    for _ in range(100):
        # create world
        population = Population()
        # simulation start
        while population.infectious_size != population.population_size\
        and population.infectious_size != 0:
            breakout += 1
            # susceptible => infectious update
            contact = Population(individuals=sample(population.individuals, MAX_CONTACT_NUMBER))
            p = 1 - (1-Beta)**contact.infectious_size
            for individual in population.filter(State.SUSCEPTIBLE):
                if random() < p:
                    individual.state = State.INFECTIOUS
            # infectious => immune update
            for individual in population.filter(State.INFECTIOUS):
                if random() < RECOVERY_RATE:
                    individual.state = State.IMMUNE
            # immune => susceptible update
            for individual in population.filter(State.IMMUNE):
                if random() < IMMUNE_REMOVE_RATE:
                    individual.state = State.SUSCEPTIBLE
            # population size update
            population.update_size()
    results.append(round(breakout/100))
    breakout = 0


print(results)

# Data for plotting

fig, ax = plt.subplots()
ax.plot(BETAS, results)

ax.set(xlabel='beta', ylabel='breakout size',
       title='Breakout size comparison with varies beta settings')
ax.grid()

fig.savefig("test.png")
plt.show()