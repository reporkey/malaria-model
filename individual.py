from enum import *
import numpy as np
from collections import deque


class State(Enum):
    S = auto()
    I = auto()
    R = auto()


class Individual:

    def __init__(self, state: State, duration=0, threshold=np.random.uniform(0, 1)):
        self.state = state
        self.duration = duration
        self.threshold = threshold

    def isSymp(self):
        return self.state == State.I and self.duration > 8