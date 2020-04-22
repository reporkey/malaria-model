import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from population import *
from parameter import Parameter
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
            if population.I_size == population.N_size \
                    or population.I_size == 0 \
                    or self.recorder.time > 3500:
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

# """ Data for plotting """
# time = np.arange(start=0, stop=time+1, step=1)
#
# """ Human """
# fig, ax = plt.subplots()
# ax.plot(time, num_I, color='red', label='I')
# ax.plot(time, num_R, color='blue', label='R')
#
# ax.set(xlabel='Time(day)', ylabel='Population')
# plt.legend()
# ax.grid()
#
# fig.savefig("human.png")
# plt.show()
#
# """ Mos """
# fig1, ax1 = plt.subplots()
# ax1.plot(time, I_m)
#
# ax1.set(xlabel='Time', ylabel='Infectivity', title='mosquitoes Infectivity')
# ax1.grid()
#
# fig1.savefig("mos.png")
# plt.show()
#
#
# """Analysis result"""
#
# mean_I = np.mean(num_I)
# mean_R = np.mean(num_R)
# mean_I_m = np.mean(I_m)
#
# print("mean_S: %d" % mean_S)
# print("mean_I: %d" % mean_I)
# print("mean_R: %d" % mean_R)
# print("mean_I_m: %f3" % mean_I_m)