class Parameter:

    def __init__(self, beta_M_H, beta_H_M, day_I_R, day_R_S, bite_per_day, life_expectancy):
        self.N = 1000000
        self.S = 900000
        self.I = 100000
        self.R = 0

        self.beta_M_H = beta_M_H
        self.beta_H_M = beta_H_M
        self.day_I_R = day_I_R
        self.day_R_S = day_R_S

        self.bite_per_day = bite_per_day
        self.life_expectancy = life_expectancy

        self.gPara = gPara()


class gPara:
    def __init__(self, n=2, k=10, o=0.6, gmax=1):
        self.n = n
        self.k = k
        self.o = o
        self.gmax = gmax