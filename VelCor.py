import matplotlib.pyplot as plt
import sys
from math import sqrt
from tqdm import tqdm
import numpy as np
# Run as python VelCor.py <filename>

_, filename = sys.argv[:2]

fp = open(filename, 'r')
lines = [u.split() for u in fp.readlines()[2:]]
fp.close()

v = []
n_temp = []

for line in lines:
    if 'END' in line:
        v.append(n_temp)
        n_temp = []

    else:
        p = [float(u) for u in line]
        # p = [float(u) for u in line[5:8]]

        n_temp.append(p)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


# for j in range(2000):
#     print(np.mean([np.linalg.norm(v[j][i]) for i in range(108)]))
# exit()
smax = 0
velcor = []
n_atoms = len(v[0])

for gap in tqdm(range(0, len(v))):
    vcc = 0
    for i in range(n_atoms):
        vcor = [dot(v[m][i], v[m + gap][i]) for m in range(len(v) - gap)]
        if not len(vcor):
            break
        vcc += (sum(vcor) / len(vcor))
    vcc /= n_atoms
    velcor.append(vcc)


plt.plot(range(1, len(velcor)+1), velcor)
plt.show()
