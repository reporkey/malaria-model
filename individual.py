from enum import *


class State(Enum):
    S = auto()
    PI = auto()
    I = auto()
    R = auto()


class Individual:
    def __init__(self, state: State):
        self.state = state
        self.duration = 0