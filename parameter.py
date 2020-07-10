import json


class Parameter:

	def __init__(self, beta_M_H, beta_H_M, day_I_R, day_R_S, bite_per_day, life_expectancy):
		self.N = 10000
		self.S = 9000
		self.I = 1000
		self.R = 0

		self.beta_M_H = beta_M_H
		self.beta_H_M = beta_H_M
		self.day_I_R = day_I_R
		self.day_R_S = day_R_S

		self.bite_per_day = bite_per_day
		self.life_expectancy = life_expectancy

		self.gPara = gPara()

	def toJson(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


class gPara:

	def __init__(self, n=2, k=10, o=0.6, gmax=1):
		self.n = n
		self.k = k
		self.o = o
		self.gmax = gmax

	def toJson(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)