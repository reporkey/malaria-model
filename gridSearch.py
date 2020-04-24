import numpy as np
import multiprocessing as mp
import json
from parameter import Parameter
from simulator import Simulator


def runSim(parameter):
	sim = Simulator(parameter)
	return sim.recorder.collectData()


class GridSearch:

	def __init__(self):
		beta_M_H = np.linspace(start=0.1, stop=0.9, num=4)
		beta_H_M = np.linspace(start=0.1, stop=0.9, num=4)
		day_I_R = np.linspace(start=20, stop=40, num=3)
		day_R_S = np.linspace(start=30, stop=100, num=3)
		bite_per_day = 1/3
		life_expectancy = 10
		index = 1
		header = "Parameters, Time(int), I, Symp, R, I_m\n"
		header += "Parameters: [N, S, I, R, betaMH, betaHM, dayIR, dayRS, biteRate, life_expectancy, G: (n, k, o, Gmax)]\n"
		for a in beta_M_H:
			for b in beta_H_M:
				for c in day_I_R:
					for d in day_R_S:
						ps = [Parameter(a, b, c, d, bite_per_day, life_expectancy) for _ in range(4)]
						with mp.Pool(processes=4) as pool:
							results = pool.map(runSim, ps)
							with open('result' + str(index) + '.json', 'w') as f:
								json.dump(results, f)
								index += 1


if __name__ == '__main__':
	gridSearch = GridSearch()
	