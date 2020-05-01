from individual import *
from numpy import random


class Population:
	def __init__(self, gPara, N=0, S=0, I=0, R=0, individuals=None):
		if individuals is None:
			self.N_size = N
			self.S_size = S
			self.I_size = I
			self.R_size = R
			self.gPara = gPara
			self.individuals = []
			self.generate()
		else:
			self.individuals = individuals
			self.update_size()

	# generate individuals
	def generate(self):
		for _ in range(self.S_size):
			self.individuals.append(Individual(state=State.S, gPara=self.gPara))
		for _ in range(self.I_size):
			self.individuals.append(Individual(state=State.I, duration=np.random.randint(20), gPara=self.gPara))
		for _ in range(self.R_size):
			self.individuals.append(Individual(state=State.R, gPara=self.gPara))

	# filter out individuals in certain state, e.g population.filter(State.I)
	# => [immune indi]
	def filter(self, state: State):
		return filter(lambda individual: (individual.state is state), self.individuals)

	def update_size(self):
		self.S_size = len(list(self.filter(State.S)))
		self.I_size = len(list(self.filter(State.I)))
		self.R_size = len(list(self.filter(State.R)))
		self.N_size = self.S_size + self.I_size + self.R_size

	def getSympNum(self):
		return [True for i in list(self.filter(State.I)) if i.duration >= 8 ].count(True)