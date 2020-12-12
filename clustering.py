from math import hypot
from typing import List, Set


class ClusterPoint:
    def __init__(self, x, y, children=None):
        self.x = x
        self.y = y
        if children is None:
            children = []
        self.linked = children
        self.done = False

    def link_to(self, child):
        self.linked.append(child)

    def dist(self, other) -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def in_range(self, other, max_dist):
        return self.dist(other) < max_dist


class Cluster:
    def __init__(self):
        self.skeleton = []

    def xy(self):
        return [(cp.x, cp.y) for cp in self.skeleton]

    def add_point(self, cp: ClusterPoint):
        self.skeleton.append(cp)

    def __len__(self):
        return len(self.skeleton)


def cluster(points, max_distance=100):
    ps: Set[ClusterPoint] = {ClusterPoint(x, y) for (x, y) in points}

    def recurse(point: ClusterPoint, bag: Set[ClusterPoint], cluster: Cluster):
        point.done = True
        cluster.add_point(point)

        close_points = [other for other in bag if point.in_range(other, max_distance)]

        for close_point in close_points:
            point.link_to(close_point)

            if close_point.done:
                continue

            bag.remove(close_point)

            recurse(close_point, bag, cluster)

    clusters: List[Cluster] = []

    while len(ps) > 0:
        p = ps.pop()
        c = Cluster()
        clusters.append(c)
        recurse(p, ps, c)
    return clusters
