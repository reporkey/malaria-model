class Mosquito:

    def __init__(self, beta, bite_per_day, life_expectancy):
        """Beta: from untreated disease: 0.40; from patent infection: 0.12"""
        self.beta = beta
        self.bite_per_day = bite_per_day
        self.life_expectancy = life_expectancy
        self.I = 0

    def update(self, population):

        S = 1 - self.I
        theta = 1 - (1-self.beta*population.I_size/population.N_size)**self.bite_per_day
        self.I = self.I + theta * S - self.I / self.life_expectancy

