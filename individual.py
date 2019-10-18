from enum import *
import numpy as np

class State(Enum):
    S = auto()
    E = auto()
    I = auto()
    R = auto()


class Individual:
    def __init__(self, state: State):
        self.state = state
        self.CDF = 0
        self.duration = 0
        self.threshold = np.random.uniform(0, 1)