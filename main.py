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
E = 0
I = 5
R = 0
beta_M_H = 0.89
beta_H_M = 0.20
lambda_E_I = 1/12
lambda_I_R = 1/200
lambda_R_S = 1/30

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
population = Population(N, S, E, I, R)
mos = Mosquito(beta=beta_H_M,
               bite_per_day=bite_per_day,
               life_expectancy=life_expectancy,
               population=population)

num_of_susceptible.append(population.S_size)
num_of_pre_infectious.append(population.E_size)
num_of_infectious.append(population.I_size)
num_of_recovery.append(population.R_size)
mosI.append(mos.I)

# simulation start
while not (population.I_size == population.N_size or population.I_size == 0 or time == 2000):

    # update mosquito
    mos.update(population)

    # susceptible => pre-infectious
    p = mos.I * mos.bite_per_day * beta_M_H
    for individual in population.filter(State.S):
        if np.random.poisson() < p:
            individual.state = State.E
            individual.duration = 0
        else:
            individual.duration += 1

    # pre-infectious update => infectious
    p = lambda_E_I
    for individual in population.filter(State.E):
        if individual.duration >= 1/p:
            individual.state = State.I
            individual.duration = 0
        else:
            individual.duration += 1

    # infectious => recovery
    p = lambda_I_R
    for individual in population.filter(State.I):
        if individual.duration >= 1/p:
            individual.state = State.R
            individual.duration = 0
        else:
            individual.duration += 1

    # recovery => susceptible
    p = lambda_R_S
    for individual in population.filter(State.R):
        if individual.duration >= 1/p:
            individual.state = State.S
            individual.duration = 0
        else:
            individual.duration += 1

    # population number update
    population.update_size()

    # for plot
    time += 1
    num_of_susceptible.append(population.S_size)
    num_of_pre_infectious.append(population.E_size)
    num_of_infectious.append(population.I_size)
    num_of_recovery.append(population.R_size)
    mosI.append(mos.I)


""" Data for plotting """
time = np.arange(start=0, stop=time+1, step=1)
fig, ax = plt.subplots()
ax.plot(time, num_of_susceptible)
ax.plot(time, num_of_pre_infectious)
ax.plot(time, num_of_infectious)
ax.plot(time, num_of_recovery)

ax.set(xlabel='Time step', ylabel='Number of infectious',
       title='SIRS (1/12, 1/200, 1/30)')
plt.legend(['S', 'E', 'I', 'R'])
ax.grid()

fig.savefig("temp.png")
plt.show()

""" Mos """
fig1, ax1 = plt.subplots()
ax1.plot(time, mosI)

ax1.set(xlabel='Time step', ylabel='I of Mos',
       title='Infectious mosquitoes')
plt.legend(['I'])
ax1.grid()

fig1.savefig("temp1.png")
plt.show()

"""Analysis result"""
mean_S = np.mean(num_of_susceptible[1000:])
mean_E = np.mean(num_of_pre_infectious[1000:])
mean_I = np.mean(num_of_infectious[1000:])
mean_R = np.mean(num_of_recovery[1000:])
mean_Mos_I = np.mean(mosI[1000:])

print("mean_S: %d" %(mean_S))
print("mean_E: %d" %(mean_E))
print("mean_I: %d" %(mean_I))
print("mean_R: %d" %(mean_R))
print("mean_Mos_I: %f3" %(mean_Mos_I))