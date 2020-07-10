# based on pengxin's paper

import numpy as np
import matplotlib.pyplot as plt

for e in range(10):

    P_int = np.random.uniform(0,10)             # inoculation size (parasites/mL)
    mu = np.random.uniform(0,35)                # mean of the initial parasite age distribution (h)
    sigma = np.random.uniform(0,20)             # SD of the initial parasite age distribution (h)
    r_P = np.random.uniform(0,100)              # parasite replication rate (unitless)
    k_d = 0                                     # rate of asexual parasite killing by PQP
    f = np.random.uniform(0,1)                  # sexual commitment rate (in percentage) (unitless)
    delta_P = np.random.uniform(0,0.2)          # death rate of asexual and sexual parasites (h^-1)
    m = np.random.uniform(0,0.1)                # maturation rate of gametocytes (h^-1)
    delta_G = np.random.uniform(0,0.1)          # death rate of sequestered gametocytes (h^-1)
    delta_Gm = np.random.uniform(0,0.1)         # death rate of circulating gametocytes (h^-1)
    a_s = 25                                    # sequestration age of asexual parasites (h)
    a_L = 42                                    # length of life cycle of asexual parasites (h)

    t = 0

    P = np.random.normal(P_int, mu, size=a_L)
    P = P.clip(min=0)
    P_G = np.zeros(a_L)
    G = np.zeros(5)
    total = np.sum(P[:a_s-2]+P_G[:a_s-2]) + G[4]
    asexual = np.array([np.sum(P[:a_s-2])])
    sexual = np.array([np.sum(P_G[:a_s-2])])
    gametocytes = np.array([G[4]])
    totals = np.array([total])

    for _ in range(500):

        t += 1

        """Asexual"""
        P = np.roll(P, 1) * np.exp(-k_d-delta_P)
        P[0] *= r_P

        """some partial becomes sexual"""
        P_G[a_s] = f * P[a_s-1]
        P[a_s] -= P_G[a_s]

        """Sexual"""
        P_G_as_temp = P_G[a_s]
        P_G = np.roll(P_G, 1) * np.exp(-delta_P)
        P_G[0] *= r_P
        P_G[a_s] = P_G_as_temp

        """Gametocytes"""
        G[0] = G[0]*np.exp(-(m+delta_G)) + (P_G[a_s-2]*np.exp(-delta_P)*(1-np.exp(-(m+delta_G))))/(m+delta_G)
        G[1] = G[1]*np.exp(-(m+delta_G)) + (m*G[0]*(1-np.exp(-(m+delta_G))))/(m+delta_G)
        G[2] = G[2]*np.exp(-(m+delta_G)) + (m*G[1]*(1-np.exp(-(m+delta_G))))/(m+delta_G)
        G[3] = G[3]*np.exp(-(m+delta_G)) + (m*G[2]*(1-np.exp(-(m+delta_G))))/(m+delta_G)
        G[4] = G[4]*np.exp(-delta_Gm) + (m*G[3]*(1-np.exp(-delta_Gm)))/delta_Gm

        total = np.sum(P[:a_s-2]+P_G[:a_s-2]) + G[4]
        asexual = np.append(asexual, np.sum(P[:a_s-2]))
        sexual = np.append(sexual, np.sum(P_G[:a_s-2]))
        gametocytes = np.append(gametocytes, [G[4]])
        totals = np.append(totals, total)

    """ Data for plotting """
    time_scales = [100, 365]
    time = np.arange(start=0, stop=500+1, step=1)
    for scale in time_scales:

        fig, ax = plt.subplots(4, 1, figsize=(12, 15))

        ax[0].plot(time[:scale], asexual[:scale])
        ax[0].plot(time[:scale], totals[:scale])
        ax[0].set(xlabel='Time step', ylabel='Number of parasites',
               title='num of parasites vs. time')
        ax[0].legend(['Asexual', 'Total'])
        ax[0].grid()

        ax[1].plot(time[:scale], sexual[:scale], color='g')
        ax[1].set(xlabel='Time step', ylabel='Number of sexual',
               title='num of sexual vs. time')
        ax[1].grid()

        ax[2].plot(time[:scale], gametocytes[:scale], color='r')
        ax[2].set(xlabel='Time step', ylabel='Number of gametocytes',
               title='num of gametocytes vs. time')
        ax[2].grid()

        ax[3].axis('off')
        ax[3].table(cellText=[["P_int", "mu", "sigma", "r_P", "f", "delta_P", "m", "delta_G", "delta_Gm"],
                              [format(P_int, '.3f'), format(mu, '.3f'), format(sigma, '.3f'),
                               format(r_P, '.3f'), format(f, '.3f'),
                               format(delta_P, '.3f'), format(m, '.3f'),
                               format(delta_G, '.3f'), format(delta_Gm, '.3f')]],
                    loc='center', cellLoc='center'
                    )


        fig.savefig("sample"+str(e)+"_"+str(scale)+".png")
        # plt.show()
