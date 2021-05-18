import matplotlib.pyplot as plt
import numpy as np
from math import inf
from config import read_config

# Change the value of the alpha or delta of the regression in the CONFIG.txt file

argv = read_config()

sigma = 3.4  # 3.4 A
epsilon = 0.238  # kcal/mol // multiply by 4184 for Joules


def min_image_vector(v1, v2):
    # vector from v1 to v2 i.e. v2 - v1
    v11 = v1 + np.array([18., 0., 0.])
    v12 = v1 + np.array([-18., 0., 0.])
    v13 = v1 + np.array([0., 18., 0.])
    v14 = v1 + np.array([0., -18., 0.])
    v15 = v1 + np.array([0., 0., 18.])
    v16 = v1 + np.array([0., 0., -18.])

    d = inf
    v = None

    for vec1 in [v1, v11, v12, v13, v14, v15, v16]:
        u = np.linalg.norm(v2-vec1)
        if u < d:
            d = u
            v = vec1

    return v, d


l = []
with open('initial_coordinates.xyz', 'r') as fp:
    fp.readline()
    fp.readline()

    l = np.array([[float(v) for v in u.split()[1:]] for u in fp.readlines()])


def U(rij):
    x = (sigma/rij)**6
    return 4*epsilon*(x)*(x - 1)


def U_sys(S):
    U_total = 0

    for i in range(len(S)):
        for j in range(i+1, len(S)):
            _, rij = min_image_vector(S[j], S[i])
            U_total += U(rij)

    return U_total


def F_1D(x):
    # 1D force
    force = 4*epsilon*((6*(sigma**6))/(x**7) - (12*(sigma**12))/(x**13))
    return -force


def F(a1, a2):
    # force due to a1 on a2
    a1, dist = min_image_vector(a1, a2)
    a = (a2-a1)/dist
    return F_1D(dist)*a


# Regression parameters
alpha = argv['regressison_alpha']
delta = argv['regressison_delta']
#############

U_total = U_sys(l)
U_new = 0

y = [U_total]

n_iter = 0
while True:
    n_iter += 1
    for i in range(len(l)):
        F_total = np.array([0., 0., 0.])

        # total force calculation
        for j in range(len(l)):
            if i != j:
                F_total += F(l[j], l[i])

        l[i] += alpha*F_total

    U_new = U_sys(l)
    y.append(U_new)
    print(n_iter, U_new - U_total, U_new)

    if abs(U_new - U_total) <= delta:
        break

    U_total = U_new

x_axis = range(len(y))
plt.plot(x_axis, y)
plt.show()

with open("initial_coord_minU.xyz", 'w+') as fp:
    fp.write('108\nmodel of argon system\n')
    for row in l:
        fp.write('C ')
        fp.write(' '.join([str(u) for u in row]) + '\n')
