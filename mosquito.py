import numpy as np
from individual import State
from scipy.stats import norm

"""
This mosquitoes model accords to [Ross A, Killeen G, Smith T (2006) Relationships between host infectivity to
mosquitoes and asexual parasite density in. Am J Trop Med Hyg 75: 32–37.]

The model from Ross maps the infectivity to the density of asexual parasites. Gametocytes (erythrocytic sexual
parasite) stage is implicitly presented. So, an additional asexual parasites development curve is required .
"""


class Mosquito:

    def __init__(self, beta, bite_per_day, life_expectancy):
        self.beta = beta
        self.bite_per_day = bite_per_day
        self.life_expectancy = life_expectancy
        self.I = 0

    def update(self, population):

        S = 1 - self.I
        theta = 1 - (1-self.beta*population.G)**self.bite_per_day
        self.I = self.I + theta * S - self.I / self.life_expectancy
