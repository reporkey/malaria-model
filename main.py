import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
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

N = 10000
S = 9990
E = 5
I = 5
R = 0
beta_M_H = 0.89
beta_H_M = 0.20
day_I_R = 20
day_R_S = 30

bite_per_day = 1/3
life_expectancy = 10

""" for plot """
time = 0
num_of_susceptible = []
num_of_pre_infectious = []
num_of_infectious = []
num_of_recovery = []
mosI = []

# create world
population = Population(N, S, I, R)
mos = Mosquito(beta=beta_H_M,
               bite_per_day=bite_per_day,
               life_expectancy=life_expectancy,
               population=population)

num_of_susceptible.append(population.S_size)
num_of_infectious.append(population.I_size)
num_of_recovery.append(population.R_size)
mosI.append(mos.I)

# simulation start
while (population.E_size + population.I_size) != population.N_size \
        and (population.E_size + population.I_size) != 0 \
        and time < 5000:

    # update mosquito
    mos.update(population)

    # susceptible => pre-infectious
    p = mos.I * mos.bite_per_day * beta_M_H
    for individual in population.filter(State.S):
        if np.random.uniform() < p:
            individual.state = State.E
            individual.duration = -2
            # threshold for G level that E => I
            # 95% CI: (0.2, 0.4) equivalent to (day 10, day 13) post inoculation
            individual.threshold = np.random.normal(0.24, 0.11)
        else:
            individual.duration += 1

    # pre-infectious => infectious
    for individual in population.filter(State.E):
        if individual.getG() > individual.threshold:
            individual.state = State.I
            # threshold for Poisson CDF that I => R
            individual.threshold = np.random.uniform(0, 1)
            individual.symptomTime = individual.duration
        else:
            individual.duration += 1

    # infectious => recovery
    rv = poisson(day_I_R)
    for individual in population.filter(State.I):
        if rv.cdf(individual.duration - individual.symptomTime) > individual.threshold:
            individual.state = State.R
            individual.duration = -2
            individual.threshold = np.random.uniform(0, 1)
        else:
            individual.duration += 1


    # recovery => susceptible
    rv = poisson(day_R_S)
    for individual in population.filter(State.R):
        if rv.cdf(individual.duration) > individual.threshold:
            individual.state = State.S
            individual.duration = -2
            individual.threshold = np.random.uniform(0, 1)
        else:
            individual.duration += 1


    # population number update
    population.update_size()

    # for plot
    time += 1
    num_of_susceptible.append(population.S_size)
    num_of_infectious.append(population.I_size)
    num_of_recovery.append(population.R_size)
    mosI.append(mos.I)


""" Data for plotting """
time = np.arange(start=0, stop=time+1, step=1)
fig, ax = plt.subplots()
ax.plot(time, num_of_susceptible, color='green', label='S')
ax.plot(time, num_of_infectious, color='orange', label='E')
ax.plot(time, num_of_infectious, color='red', label='I')
ax.plot(time, num_of_recovery, color='blue', label='R')

ax.set(xlabel='Time step', ylabel='Number of I')
plt.legend()
ax.grid()

fig.savefig("temp.png")
plt.show()

""" Mos """
fig1, ax1 = plt.subplots()
ax1.plot(time, mosI)

ax1.set(xlabel='Time step', ylabel='I of Mos', title='mosquitoes Infectivity')
ax1.grid()

fig1.savefig("temp1.png")
plt.show()


"""Analysis result"""

mean_S = np.mean(num_of_susceptible)
mean_I = np.mean(num_of_infectious)
mean_R = np.mean(num_of_recovery)
mean_Mos_I = np.mean(mosI)

print("mean_S: %d" % mean_S)
print("mean_I: %d" % mean_I)
print("mean_R: %d" % mean_R)
print("mean_Mos_I: %f3" % mean_Mos_I)