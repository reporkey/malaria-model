import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from population import *
from mosquito import *
from recorder import Recorder


class Simulator:

    def __init__(self, parameter):
        self.parameter = parameter
        self.recorder = Recorder(parameter)
        self.simulator()

    def simulator(self):

        # create world
        population = Population(N=self.parameter.N, S=self.parameter.S, I=self.parameter.I, R=self.parameter.R,
                                gPara=self.parameter.gPara)
        mos = Mosquito(beta=self.parameter.beta_H_M,
                       bite_per_day=self.parameter.bite_per_day,
                       life_expectancy=self.parameter.life_expectancy)

        # simulation start
        while True:
            if self.recorder.ifTerminate():
                return

            # record data
            self.recorder.time += 1
            self.recorder.append(i=population.I_size, symp=population.getSympNum(), r=population.R_size, im=mos.I)

            # update mosquito
            mos.update(population)

            # susceptible => infectious
            p = mos.I * mos.bite_per_day * self.parameter.beta_M_H
            for individual in population.filter(State.S):
                if np.random.uniform() < p:
                    individual.state = State.I
                    # threshold for Poisson CDF that I => R
                    individual.threshold = np.random.uniform(0, 1)
                    individual.duration = -1
                else:
                    individual.duration += 1

            # infectious => recovery
            rv = poisson(self.parameter.day_I_R)
            for individual in population.filter(State.I):
                if rv.cdf(individual.duration) > individual.threshold:
                    individual.state = State.R
                    individual.duration = -1
                    individual.threshold = np.random.uniform(0, 1)
                    individual.reset()
                else:
                    individual.duration += 1
                    individual.update()

            # recovery => susceptible
            rv = poisson(self.parameter.day_R_S)
            for individual in population.filter(State.R):
                if rv.cdf(individual.duration) > individual.threshold:
                    individual.state = State.S
                    individual.duration = -1
                    individual.threshold = np.random.uniform(0, 1)
                else:
                    individual.duration += 1

            # population number update
            population.update_size()