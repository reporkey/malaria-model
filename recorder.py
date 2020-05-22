import json


class Recorder:

	def __init__(self, p):
		self.i = []
		self.symp = []
		self.r = []
		self.im = []
		self.time = -1
		self.parameters = p
		#[p.N, p.S, p.i, p.r, p.beta_M_H, p.beta_H_M, p.day_I_R, p.day_R_S,
  #                         p.bite_per_day, p.life_expectancy,
  #                         (p.gPara.n, p.gPara.k, p.gPara.o, p.gPara.gmax)]

	def append(self, i: int, symp: int, r: int, im):
		self.i.append(i)
		self.symp.append(symp)
		self.r.append(r)
		self.im.append(im)

	def collectData(self):
		data = {}
		data["parameter"] = self.parameters.toJson()
		data["time"] = self.time
		data["i"] = self.i
		data["symp"] = self.symp
		data["r"] = self.r
		data["im"] = self.im
		return data

	def ifTerminate(self):
		if self.time > 0:
			if self.i[-1] == 0 or self.i[-1] == self.parameters.N:
				return True
		if self.time > 1200:
			return True
		if self.time > 300:
			if max(self.i[-300:]) - min(self.i[-300:]) < 0.02 * self.parameters.N:
				return True
		return False