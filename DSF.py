from tqdm import tqdm
import matplotlib.pyplot as plt
import sys
from math import sqrt, exp

import numpy as np

_, filename = sys.argv[:2]
PI = 3.1416
a = 1e-2


fp = open(filename, 'r')
lines = [u.split() for u in fp.readlines()[2:]]
fp.close()

d = []

n_temp = []


for line in lines:
    if 'END' in line:
        d.append(n_temp)
        n_temp = []

    else:
        p = [float(u)*1e10 for u in line]
        n_temp.append(p)


def delta(x):
    return exp(-((x/a)**2))/(a*sqrt(PI))


n_atoms = len(d[0])

# Van Hove


def G(r, t):
    G_r = 0
    for i in range(n_atoms):
        for j in range(n_atoms):
            rj = d[t][j]
            ri = d[0][i]

            vec = [rj[0] - ri[0],
                   rj[1] - ri[1],
                   rj[2] - ri[2]]
            x = sqrt(sum(u**2 for u in vec))
            G_r += delta(x-r)

    G_r /= (n_atoms**3)
    return G_r


def S():
    G_r_t = np.zeros((len(d), 400))

    for time in tqdm(range(len(d))):
        for r in range(400):
            G_r_t[time][r] = G(r/10, time)

    F_k_t = np.array([np.fft.fft(row) for row in G_r_t])
    F_k_t_T = F_k_t.T

    S_k_w = np.array([np.fft.fft(row) for row in F_k_t_T])

    return S_k_w  # Returns it in form S_k_w[k][w]


S_arr = S()
colors = ['red', 'orange', 'green', 'lightseagreen', 'dodgerblue',
          'navy', 'slateblue', 'violet', 'magenta', 'deeppink', 'cyan']
print(S_arr.shape)
x_axis = list(range(S_arr.shape[0]))

i = 0

for w in range(0, S_arr.shape[1], S_arr.shape[1]//10):
    try:
        y_axis = [abs(u) for u in (S_arr[:, w]).T]
        plt.plot(x_axis, y_axis, colors[i])
        i += 1
    except:
        plt.show()
        exit()

plt.show()
