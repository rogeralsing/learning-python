from math import hypot


class ClusterPoint:
    def __init__(self, x, y, children=None):
        self.x = x
        self.y = y
        if children is None:
            children = []
        self.children = children


class Cluster:
    def __init__(self):
        self.skeleton = []

    def xy(self):
        return [(cp.x, cp.y) for cp in self.skeleton]

    def add(self, cp):
        self.skeleton.append(cp)


def cluster(points, max_distance=100):
    ps = [ClusterPoint(x, y) for (x, y) in points]

    def dist(p1, p2):
        return hypot(p1.x - p2.x, p1.y - p2.y)

    def recurse(current_point, bag, current_cluster):
        bag.remove(current_point)
        current_cluster.add(current_point)

        for child_point in filter(lambda p2: dist(current_point, p2) < max_distance, bag):
            current_point.children.append(child_point)
            recurse(child_point, bag, current_cluster)

    clusters = []
    while len(ps) > 0:
        p = ps[0]
        c = Cluster()
        clusters.append(c)
        recurse(p, ps, c)
    return clusters
