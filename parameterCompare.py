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
		beta_M_H = [0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 0.99]
		beta_H_M = [0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 0.99]
		day_I_R = np.linspace(start=10, stop=40, num=5)
		day_R_S = np.linspace(start=30, stop=100, num=5)
		bite_per_day = 1/3
		life_expectancy = 10

		index = 1
		header = "Parameters, Time(int), I, Symp, R, I_m\n"
		header += "Parameters: [N, S, I, R, betaMH, betaHM, dayIR, dayRS, biteRate, life_expectancy, G: (n, k, o, Gmax)]\n"


		for i in beta_M_H:
			for j in beta_H_M:
				ps = [Parameter(i, j, 30, 50, bite_per_day, life_expectancy) for _ in range(6)]
				with mp.Pool(processes=6) as pool:
					results = pool.map(runSim, ps)
				with open('./data/raw1/data' + str(index) + '.json', 'w') as f:
					json.dump(results, f)
				print("beta_M_H:", i, "beta_H_M:", j)
				index += 1



if __name__ == '__main__':
	parameterCompare = ParameterCompare()
	#p = Parameter(0.8, 0.3, 30, 50, 1/3, 10)
	#sim = Simulator(p)