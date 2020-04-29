import numpy as np
import multiprocessing as mp
import json
import matplotlib.pyplot as plt
from parameter import Parameter
from simulator import Simulator


def runSim(parameter):
    sim = Simulator(parameter)
    return sim.recorder.collectData()


class ParameterCompare:

    def __init__(self):
        beta_M_H = np.linspace(start=0.1, stop=0.9, num=10)
        beta_H_M = np.linspace(start=0.1, stop=0.9, num=10)
        day_I_R = np.linspace(start=10, stop=40, num=5)
        day_R_S = np.linspace(start=30, stop=100, num=5)
        bite_per_day = 1/3
        life_expectancy = 10

        index = 1
        header = "Parameters, Time(int), I, Symp, R, I_m\n"
        header += "Parameters: [N, S, I, R, betaMH, betaHM, dayIR, dayRS, biteRate, " \
                  "life_expectancy, G: (n, k, o, Gmax)]\n"

        for i in beta_M_H:
            ps = [Parameter(i, 0.3, 30, 50, bite_per_day, life_expectancy) for _ in range(10)]
            with mp.Pool(processes=10) as pool:
                results = pool.map(runSim, ps)
                print(results)
                with open('result' + str(index) + '.json', 'w') as f:
                    json.dump(results, f)

        for i in beta_H_M:
            ps = [Parameter(0.8, i, 30, 50, bite_per_day, life_expectancy) for _ in range(10)]
            with mp.Pool(processes=10) as pool:
                results = pool.map(runSim, ps)
                print(results)
                with open('result' + str(index) + '.json', 'w') as f:
                    json.dump(results, f)


if __name__ == '__main__':
    parameterCompare = ParameterCompare()
    # p = Parameter(0.8, 0.3, 30, 50, 1/3, 10)
    # sim = Simulator(p)

    # """ Plot """
    # time = np.arange(start=0, stop=sim.recorder.collectData()["time"]+1, step=1)
    # print(sim.recorder.collectData()["time"])
    # print(len(sim.recorder.collectData()["I"]))
    # """ Human """
    # fig, ax = plt.subplots()
    # ax.plot(time, sim.recorder.collectData()["I"], color='red', label='I')
    # ax.plot(time, sim.recorder.collectData()["R"], color='blue', label='R')
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
    # ax1.plot(time, sim.recorder.collectData()["Im"])
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
    # mean_I = np.mean(sim.recorder.collectData()["I"])
    # mean_R = np.mean(sim.recorder.collectData()["R"])
    # mean_I_m = np.mean(sim.recorder.collectData()["Im"])
    #
    # print("mean_I: %d" % mean_I)
    # print("mean_R: %d" % mean_R)
    # print("mean_I_m: %f3" % mean_I_m)