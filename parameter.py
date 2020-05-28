import json


class Parameter:

	def __init__(self, beta_M_H, beta_H_M, day_I_R, day_R_S, bite_per_day, life_expectancy):
		self.N = 5000
		self.S = 4500
		self.I = 500
		self.R = 0

		self.beta_M_H = beta_M_H
		self.beta_H_M = beta_H_M
		self.day_I_R = day_I_R
		self.day_R_S = day_R_S

		self.bite_per_day = bite_per_day
		self.life_expectancy = life_expectancy

	def toJson(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)