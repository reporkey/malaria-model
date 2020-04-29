
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

    def ifTerminate(self):
        if self.time > 500:
            if max(self.I[-500:]) - min(self.I[-500:]) < 0.03 * self.Parameters[0]:
                return True
        elif self.time > 0:
            if self.I[-1] == 0 or self.I[-1] == self.Parameters[0]:
                return True
        elif self.time > 2000:
            return True
        return False
