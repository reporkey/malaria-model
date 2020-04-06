from enum import *
import numpy as np
from collections import deque
from scipy.stats import norm


class State(Enum):
    S = auto()
    I = auto()
    R = auto()


n = 2
k = 10
o = 0.6
Gmax = 1

beta1 = 1
beta2 = 0.46
beta3 = 0.17

sigma = 3.91
rho = 0.00031


class Individual:

    def __init__(self, state: State, duration=0, threshold=np.random.uniform(0, 1)):
        self.state = state
        self.duration = duration
        self.threshold = threshold
        self.g = 0
        self.asexual = deque([0] * 20, maxlen=20)
        # self.infectivity = 0

    # def updateAsexual(self):
    #     x = self.duration
    #     asexual = (x ** n / (x ** n + k ** n) - o / (1 + o)) * (1 + o) * Gmax
    #     self.asexual.append(max(asexual, 0))
    #     gamma = beta1 * self.asexual[-10] + beta2 * self.asexual[-15] + beta3 * self.asexual[-20]
    #     self.infectivity = norm.cdf(np.log(gamma * rho) / sigma)

    def update(self):
        x = self.duration
        self.g = (x ** n / (x ** n + k ** n) - o / (1 + o)) * (1 + o) * Gmax

    def getI(self):
        return

    def reset(self):
        self.g = 0
        self.asexual = deque([0] * 20, maxlen=20)
