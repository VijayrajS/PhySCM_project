import matplotlib.pyplot as plt
import sys
from math import sqrt, exp

_, filename = sys.argv[:2]
PI = 3.1416
a = 1e-2

max_r = 400

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


def G_r_func(t):
    G_r_vs_R = [0 for _ in range(max_r)]
    for r in range(max_r):
        G_val = G(r/10, t)
        G_r_vs_R[r] = G_val
    return G_r_vs_R


x_axis = [u/10 for u in range(max_r)]

y_axes = []
colors = ['red', 'orange', 'green', 'lightseagreen', 'dodgerblue',
          'navy', 'slateblue', 'violet', 'magenta', 'deeppink', 'red']
i = 0
for t in range(0, len(d), int(len(d)/11)):
    print(t)
    if i >= len(colors):
        break
    if t != 0:
        y = G_r_func(t)
        plt.plot(x_axis, y, colors[i])
    i += 1

plt.gca().legend([str(u) for u in range(22, len(d), int(len(d)/11))])
plt.show()
