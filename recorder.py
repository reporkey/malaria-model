import numpy as np


class Recorder:

    def __init__(self, p):
        self.I = []
        self.symp = []
        self.R = []
        self.Im = []
        self.time = -1
        self.Parameters = [p.N, p.S, p.I, p.R, p.beta_M_H, p.beta_H_M, p.day_I_R, p.day_R_S,
                           p.bite_per_day, p.life_expectancy,
                           (p.gPara.n, p.gPara.k, p.gPara.o, p.gPara.gmax)]

    def append(self, i: int, symp: int, r: int, im):
        self.I.append(i)
        self.symp.append(symp)
        self.R.append(r)
        self.Im.append(im)

    def collectData(self):
        data = {}
        data["parameter"] = self.Parameters
        data["time"] = self.time
        data["I"] = self.I
        data["symp"] = self.symp
        data["R"] = self.R
        data["Im"] = self.Im
        return data
