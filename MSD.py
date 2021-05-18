
import matplotlib.pyplot as plt
import sys
from math import sqrt

from tqdm import tqdm
from config import read_config

argv = read_config()
# Run as python MSD.py <filename>
_, filename = sys.argv[:2]

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
        p = [float(u) for u in line]
        n_temp.append(p)


def msd_t(t1, t2):
    N = len(d[0])
    s = 0
    for i in range(0, N):
        r_ = (d[t2][i][0] - d[t1][i][0])**2 + (d[t2][i][1] -
                                               d[t1][i][1])**2 + (d[t2][i][2] - d[t1][i][2])**2
        s += r_

    return s/N


plott = []


def msd():
    n = len(d)
    for t in tqdm(range(1, n-1)):
        msd_val = 0
        for j in range(0, n-t):
            msd_val += msd_t(j, j + t)

        msd_val /= (n-t)
        plott.append(msd_val)


msd()

plt.plot(range(1, len(plott)+1), plott)

D_c = (plott[-1] - plott[len(plott)+1-500])/(500*argv["dt"])
print(D_c)

plt.show()
