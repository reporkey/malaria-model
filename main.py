from functools import reduce
from enum import *
from random import *
import numpy as np

N = 100                      # Population size
SUSCEPTIBLE_SIZE = 95
INFECTIOUS_SIZE = 5
IMMUNE_SIZE = 0

Beta = 0.1                  # Rate at which two specific individuals come into effective contact
RECOVERY_RATE = 0.2
IMMUNE_REMOVE_RATE = 0.2

MAX_CONTACT_NUMBER = 10    # Max number of contacted individual with a single per time unit

TOTAL_TIME = 10

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
        for i in range(self.susceptible_size):
            self.individuals.append(Individual(state=State.SUSCEPTIBLE))
        for i in range(self.infectious_size):
            self.individuals.append(Individual(state=State.INFECTIOUS))
        for i in range(self.immune_size):
            self.individuals.append(Individual(state=State.IMMUNE))

    # filter out individuals in certain state, e.g population.filter(State.IMMUNE) => [immune indi]
    def filter(self, state: State):
        return filter(lambda individual: (individual.state is state), self.individuals)

    def reduce(self, state: State):
        return reduce()
    def update_size(self):
        self.susceptible_size = len(list(self.filter(State.SUSCEPTIBLE)))
        self.infectious_size = len(list(self.filter(State.INFECTIOUS)))
        self.immune_size = len(list(self.filter(State.IMMUNE)))
        self.population_size = self.susceptible_size + self.infectious_size + self.immune_size

# create world
population = Population()
time = 0
# simulation start
while population.infectious_size != population.population_size\
and population.infectious_size != 0:
    time += 1
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

print(time)
