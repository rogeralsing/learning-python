from math import hypot


def cluster(points, max_distance=100):
    def dist(p1, p2):
        return hypot(p1[0] - p2[0], p1[1] - p2[1])

    def recurse(current_point, bag, current_cluster):
        bag.remove(current_point)
        current_cluster.append(current_point)

        for m in filter(lambda p2: dist(current_point, p2) < max_distance, bag):
            recurse(m, bag, current_cluster)

    clusters = []
    while len(points) > 0:
        p = points[0]
        c = []
        clusters.append(c)
        recurse(p, points, c)
    return clusters
