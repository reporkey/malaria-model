class Mosquito:

    def __init__(self, beta, bite_per_day):
        """Beta: from untreated disease: 0.40; from patent infection: 0.12"""
        self.beta = beta
        self.frac_I = 0
        self.bite_per_day = bite_per_day

    def update(self, population):
        self.frac_I = self.beta * self.bite_per_day * population.I_size / population.N_size
