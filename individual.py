from enum import *
import numpy as np
from collections import deque


class State(Enum):
    S = auto()
    I = auto()
    R = auto()


class Individual:

    def __init__(self, state: State, gPara, duration=0, threshold=np.random.uniform(0, 1)):
        self.state = state
        self.duration = duration
        self.threshold = threshold
        self.g = 0
        self.gPara = gPara

    def update(self):
        x = self.duration
        n = self.gPara.n
        k = self.gPara.k
        o = self.gPara.o
        gmax = self.gPara.gmax
        self.g = (x ** n / (x ** n + k ** n) - o / (1 + o)) * (1 + o) * gmax

    def isSymp(self):
        return self.state == State.I and self.duration > 8

    def resetg(self):
        self.g = 0