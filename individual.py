from enum import *
import numpy as np


class State(Enum):
    S = auto()
    E = auto()
    I = auto()
    R = auto()


n = 2
k = 10
o = 0.6
Gmax = 1


class Individual:

    def __init__(self, state: State, duration=0, threshold=np.random.uniform(0, 1)):
        self.state = state
        self.duration = duration
        self.threshold = threshold

    def getG(self):
        if self.state == State.I or self.state == State.E:
            x = self.duration
            G = (x ** n / (x ** n + k ** n) - o / (1 + o)) * (1 + o) * Gmax
        else:
            G = 0
        return G if G >= 0 else 0
