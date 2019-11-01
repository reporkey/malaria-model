from individual import State

class Mosquito:

    def __init__(self, beta, bite_per_day, life_expectancy, population):
        """Beta: from untreated disease: 0.40; from patent infection: 0.12"""
        self.beta = beta
        self.bite_per_day = bite_per_day
        self.life_expectancy = life_expectancy
        self.I = self.beta * self.bite_per_day * population.I_size / population.N_size

    def update(self, population):

        I = sum([i.getG() for i in population.filter(State.S)])

        # 1/10 mos die, replaced by (1-1/10) new born healthy mos + new infections
        self.I = self.I * (1 - 1/self.life_expectancy) + \
                 (1-self.I) * self.beta * self.bite_per_day * I / population.N_size


