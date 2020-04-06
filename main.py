import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
from population import *
from individual import *
from mosquito import *

N = 10000
S = 7000
I = 3000
R = 0
beta_M_H = 0.89
beta_H_M = 0.20
day_I_R = 20
day_R_S = 30

bite_per_day = 1/2
life_expectancy = 10

""" for plot """
time = -1
num_S = []
num_I = []
num_R = []
I_m = []

# create world
population = Population(N=N, S=S, I=I, R=R)
mos = Mosquito(beta=beta_H_M,
               bite_per_day=bite_per_day,
               life_expectancy=life_expectancy,
               population=population)

# simulation start
while population.I_size != population.N_size \
        and population.I_size != 0 \
        and time < 5000:

    # for plot
    time += 1
    num_S.append(population.S_size)
    num_I.append(population.I_size)
    num_R.append(population.R_size)
    I_m.append(mos.I)

    # update mosquito
    mos.update(population)

    # susceptible => infectious
    p = mos.I * mos.bite_per_day * beta_M_H
    newI = 0
    for individual in population.filter(State.S):
        if np.random.uniform() < p:
            newI += 1
            individual.state = State.I
            # threshold for Poisson CDF that I => R
            individual.threshold = np.random.uniform(0, 1)
            individual.duration = -1
        else:
            individual.duration += 1
    print("p:", p)
    print("newI:", newI)
    # infectious => recovery
    rv = poisson(day_I_R)
    newR = 0
    for individual in population.filter(State.I):
        if rv.cdf(individual.duration) > individual.threshold:
            newR += 1
            individual.state = State.R
            individual.duration = -1
            individual.threshold = np.random.uniform(0, 1)
            individual.reset()
        else:
            individual.duration += 1
            individual.update()
    print("newR:", newR)

    # recovery => susceptible
    rv = poisson(day_R_S)
    for individual in population.filter(State.R):
        if rv.cdf(individual.duration) > individual.threshold:
            individual.state = State.S
            individual.duration = -1
            individual.threshold = np.random.uniform(0, 1)
        else:
            individual.duration += 1


    # population number update
    population.update_size()
    print(population.N_size, population.I_size)


""" Data for plotting """
time = np.arange(start=0, stop=time+1, step=1)

""" Human """
fig, ax = plt.subplots()
ax.plot(time, num_S, color='green', label='S')
ax.plot(time, num_I, color='red', label='I')
ax.plot(time, num_R, color='blue', label='R')

ax.set(xlabel='Time(day)', ylabel='Population')
plt.legend()
ax.grid()

fig.savefig("human.png")
plt.show()

""" Mos """
fig1, ax1 = plt.subplots()
ax1.plot(time, I_m)

ax1.set(xlabel='Time', ylabel='Infectivity', title='mosquitoes Infectivity')
ax1.grid()

fig1.savefig("mos.png")
plt.show()


"""Analysis result"""

mean_S = np.mean(num_S)
mean_I = np.mean(num_I)
mean_R = np.mean(num_R)
mean_I_m = np.mean(I_m)

print("mean_S: %d" % mean_S)
print("mean_I: %d" % mean_I)
print("mean_R: %d" % mean_R)
print("mean_I_m: %f3" % mean_I_m)