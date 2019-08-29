from random import *
import numpy as np
import matplotlib.pyplot as plt
from population import *
from individual import *
from mosquito import *

'''
Example of Influenza
This model ignores:
pre-infectious, age pattern
vaccine(p.126)?

Equestions(p.334)
'''
# R0 = 2                                  # p.30,75,79
# D_I = 2         # duration of I         # p.30
# ce = R0/D_I     # effective contact     # p.32
# Beta = R0/N/D_I                         # p.32
# Lamda = Beta*I                          # p.32

N = 1000
S = 995
PI = 0
I = 5
R = 0
beta_M_H = 0.89
beta_H_M = 0.40
lambda_PI_I = 1/12
lambda_I_R = 1/200
bite_per_day = 1/3

""" for plot """
time = 0
num_of_susceptible = []
num_of_pre_infectious = []
num_of_infectious = []
num_of_recovery = []

# create world
mos = Mosquito(beta=beta_H_M, bite_per_day=bite_per_day)
population = Population(N, S, PI, I, R)

num_of_susceptible.append(population.S_size)
num_of_pre_infectious.append(population.PI_size)
num_of_infectious.append(population.I_size)
num_of_recovery.append(population.R_size)

# simulation start
while population.I_size != population.N_size and population.I_size != 0:

    # update mosquito
    mos.update(population)

    # susceptible => pre-infectious
    p = mos.frac_I * mos.bite_per_day * beta_M_H
    for individual in population.filter(State.S):
        if random() < p:
            individual.state = State.PI
            individual.duration = 0
        else:
            individual.duration += 1

    # pre-infectious update => infectious
    p = lambda_PI_I
    for individual in population.filter(State.PI):
        if random() < p:
            individual.state = State.I
            individual.duration = 0
        else:
            individual.duration += 1

    # infectious => recovery
    p = lambda_I_R
    for individual in population.filter(State.I):
        if random() < p:
            individual.state = State.R
            individual.duration = 0
        else:
            individual.duration += 1

    # population number update
    population.update_size()

    # for plot
    time += 1
    num_of_susceptible.append(population.S_size)
    num_of_pre_infectious.append(population.PI_size)
    num_of_infectious.append(population.I_size)
    num_of_recovery.append(population.R_size)


""" Data for plotting """
time = np.arange(start=0, stop=time+1, step=1)
fig, ax = plt.subplots()
ax.plot(time, num_of_susceptible)
ax.plot(time, num_of_pre_infectious)
ax.plot(time, num_of_infectious)
ax.plot(time, num_of_recovery)

ax.set(xlabel='time step', ylabel='number of infectious',
       title='Trend of SIR through time')
plt.legend(['num_of_susceptible', 'num_of_pre_infectious', 'num_of_infectious', 'num_of_recovery'])

ax.grid()

fig.savefig("test.png")
plt.show()