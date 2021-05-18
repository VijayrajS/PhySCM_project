import numpy as np

n = 108
d = 3.4
side = 18


def dist(new_point, points, r_threshold):
    for point in points:
        dist = np.sqrt(np.sum(np.square(new_point-point)))
        np1 = [point[0]-18, point[1], point[2]]
        np2 = [point[0]+18, point[1], point[2]]
        np3 = [point[0], point[1]-18, point[2]]
        np4 = [point[0], point[1]+18, point[2]]
        np5 = [point[0], point[1], point[2]-18]
        np6 = [point[0], point[1], point[2]+18]

        lx1 = np.sqrt(np.sum(np.square(np1-new_point)))
        lx2 = np.sqrt(np.sum(np.square(np2-new_point)))
        lx3 = np.sqrt(np.sum(np.square(np3-new_point)))
        lx4 = np.sqrt(np.sum(np.square(np4-new_point)))
        lx5 = np.sqrt(np.sum(np.square(np5-new_point)))
        lx6 = np.sqrt(np.sum(np.square(np6-new_point)))

        cond = lx1 < r_threshold or lx2 < r_threshold or lx3 < r_threshold or lx4 < r_threshold or lx5 < r_threshold or lx6 < r_threshold

        if dist < r_threshold or cond:
            return False
    return True


def RandX(N, r_threshold):
    points = []
    scope = np.arange(-(side//2), (side//2), 0.01)
    while len(points) < N:
        print(len(points))
        new_point = np.random.choice(scope, 3)
        if dist(new_point, points, r_threshold):
            points.append(new_point)
    return points


with open('initial_coordinates.xyz', 'w') as fp:
    fp.write(str(n)+'\nmodel of argon system\n')
    for points in RandX(n, d):
        fp.write('C ')
        fp.write(' '.join([str(round(u, 2)) for u in points]) + '\n')
