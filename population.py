from individual import *
from numpy import random


class Population:
    def __init__(self, N=0, S=0, E=0, I=0, R=0, individuals=None):
        if individuals is None:
            self.N_size = N
            self.S_size = S
            self.E_size = E
            self.I_size = I
            self.R_size = R
            self.individuals = []
            self.generate()
        else:
            self.individuals = individuals
            self.update_size()

    # generate individuals
    def generate(self):
        for _ in range(self.S_size):
            self.individuals.append(Individual(state=State.S))
        for _ in range(self.E_size):
            self.individuals.append(Individual(state=State.E, duration=np.random.choice(28), threshold=np.random.normal(0.24, 0.11)))
        for _ in range(self.I_size):
            self.individuals.append(Individual(state=State.I, duration=np.random.randint(13, 28), threshold=np.random.uniform(0, 1)))
            self.individuals.symptomTime = 13
        for _ in range(self.R_size):
            self.individuals.append(Individual(state=State.R))

    # filter out individuals in certain state, e.g population.filter(State.I) => [immune indi]
    def filter(self, state: State):
        return filter(lambda individual: (individual.state is state), self.individuals)

    def update_size(self):
        self.S_size = len(list(self.filter(State.S)))
        self.E_size = len(list(self.filter(State.E)))
        self.I_size = len(list(self.filter(State.I)))
        self.R_size = len(list(self.filter(State.R)))
        self.N_size = self.S_size + self.I_size + self.R_size
