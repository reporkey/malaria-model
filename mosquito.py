import numpy as np
from individual import State
from scipy.stats import norm

"""
This mosquitoes model accords to [Ross A, Killeen G, Smith T (2006) Relationships between host infectivity to
mosquitoes and asexual parasite density in. Am J Trop Med Hyg 75: 32–37.]

The model from Ross maps the infectivity to the density of asexual parasites. Gametocytes (erythrocytic sexual
parasite) stage is implicitly presented. So, an additional asexual parasites development curve is required .
"""

# sigma = 3.91
# rho = 0.00031


class Mosquito:

    def __init__(self, beta, bite_per_day, life_expectancy, population):
        """Beta: from untreated disease: 0.40; from patent infection: 0.12"""
        self.beta = beta
        self.bite_per_day = bite_per_day
        self.life_expectancy = life_expectancy
        self.I = 0

    def update(self, population):

        # Approach 1:
        S = 1 - self.I
        G = sum([i.g for i in population.individuals]) / population.N_size
        theta = 1 - (1-self.beta*G)**self.bite_per_day
        self.I = self.I + theta * S - self.I / self.life_expectancy

        # image the the g is asexual level

        # the probability of containing 1+ gametocytes in one bitten

        # asexual = np.sum([each.infectivity for each in population.filter(State.I)]) / population.N_size
        #
        # self.I = norm.cdf(np.log(asexual * rho) / sigma)