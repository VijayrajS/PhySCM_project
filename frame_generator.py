import numpy as np
from math import sqrt, inf

from tqdm import tqdm
from copy import deepcopy
from config import read_config

np.random.seed(69)

# Change the value of the Temperature, timestep, or number of frames in the CONFIG.txt file

argv = read_config()

# Constants
m = 6.633359936e-26  # mass of argon atom
K = 1.38e-23  # boltzmann constant
T = argv['temperature']

sigma_vel = sqrt(K*T)/sqrt(m)
mu_vel = 0

sigma = 3.4e-10
epsilon = 1.66e-21

dt = argv['dt']  # frame time gap

# * Utility functions


def min_image_vector(v1, v2):
    # * minimum image vector from v1 to v2 i.e. v2 - v1
    # * For periodic boundary conditions
    v11 = v1 + np.array([18e-10, 0., 0.])
    v12 = v1 + np.array([-18e-10, 0., 0.])
    v13 = v1 + np.array([0., 18e-10, 0.])
    v14 = v1 + np.array([0., -18e-10, 0.])
    v15 = v1 + np.array([0., 0., 18e-10])
    v16 = v1 + np.array([0., 0., -18e-10])

    d = inf
    vmin = None

    for vec1 in [v1, v11, v12, v13, v14, v15, v16]:
        u = np.linalg.norm(v2-vec1)
        if u < d:
            d = u
            vmin = vec1

    return vmin, d


def F_1D(x):
    # * Magnitude of force
    force = 4*epsilon*((6*(sigma**6))/(x**7) - (12*(sigma**12))/(x**13))
    return -force


def F(a1, a2):
    # * force vector due to a1 on a2
    a1, dist = min_image_vector(a1, a2)
    a = (a2-a1)/dist
    return F_1D(dist)*a


# * Initial velocity setting
vx = np.random.normal(0, sigma_vel, 107)
vy = np.random.normal(0, sigma_vel, 107)
vz = np.random.normal(0, sigma_vel, 107)
vx = np.append(vx, -sum(vx))
vy = np.append(vy, -sum(vy))
vz = np.append(vz, -sum(vz))

######

# * Reading initial config

r_t = []
with open('initial_coord_minU.xyz', 'r') as fp:
    fp.readline()
    fp.readline()

    r_t = np.array([[float(v)*1e-10 for v in u.split()[1:]]
                   for u in fp.readlines()])
    v_t = np.array([(vx[i], vy[i], vz[i]) for i in range(108)])


frames_r = [deepcopy(r_t)]
frames_v = [deepcopy(v_t)]

a_t = np.zeros(r_t.shape)
# Calculating initial acceleration

for i in range(len(r_t)):
    F_total = np.array([0., 0., 0.])

    # total force calculation
    for j in range(r_t.shape[0]):
        if i != j:
            F_total += F(r_t[j], r_t[i])

    a_t[i] = F_total/m

####


def verlet_update():
    a_t_i_arr = []

    for i in range(len(r_t)):
        a_t_i = a_t[i]
        r_t[i] = r_t[i] + dt*v_t[i] + 0.5*dt*dt*a_t_i
        a_t_i_arr.append(a_t_i)

        # Sum up forces and get net acceleration
    for i in range(len(r_t)):
        F_total = np.array([0., 0., 0.])

        # total force calculation
        for j in range(len(r_t)):
            if i != j:
                F_total += F(r_t[j], r_t[i])

        a_t[i] = F_total/m

    for i in range(len(r_t)):
        v_t[i] = v_t[i] + 0.5*(a_t[i] + a_t_i_arr[i])*dt


n_frames = int(argv['n_frames'])

for _ in tqdm(range(n_frames-1)):
    verlet_update()
    frames_r.append(deepcopy(r_t))
    frames_v.append(deepcopy(v_t))

with open("r_frames.xyz", 'w+') as fp:
    fp.write('108\nmodel of argon system\n')
    for frame in frames_r:
        for row in frame:
            fp.write(' '.join([str(u) for u in row]) + '\n')
        fp.write('END\n')

with open("v_frames.xyz", 'w+') as fp:
    fp.write('108\nmodel of argon system\n')
    for frame in frames_v:
        for row in frame:
            fp.write(' '.join([str(u) for u in row]) + '\n')
        fp.write('END\n')
