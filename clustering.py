from math import hypot
from typing import List, Set


class ClusterPoint:
    def __init__(self, x, y, children=None):
        self.x = x
        self.y = y
        if children is None:
            children = []
        self.children = children

    def add_child(self, child):
        self.children.append(child)


class Cluster:
    def __init__(self):
        self.skeleton = []

    def xy(self):
        return [(cp.x, cp.y) for cp in self.skeleton]

    def add_point(self, cp: ClusterPoint):
        self.skeleton.append(cp)


def cluster(points, max_distance=100):
    ps: Set[ClusterPoint] = {ClusterPoint(x, y) for (x, y) in points}

    def dist(p1: ClusterPoint, p2: ClusterPoint) -> float:
        return hypot(p1.x - p2.x, p1.y - p2.y)

    def recurse(current_point: ClusterPoint, bag: Set[ClusterPoint], current_cluster: Cluster):
        current_cluster.add_point(current_point)

        children = list(filter(lambda p2: dist(current_point, p2) < max_distance, bag))

        for child_point in children:
            if child_point not in bag:
                continue

            bag.remove(child_point)

            current_point.add_child(child_point)
            recurse(child_point, bag, current_cluster)

    clusters: List[Cluster] = []

    while len(ps) > 0:
        p = ps.pop()
        c = Cluster()
        clusters.append(c)
        recurse(p, ps, c)
    return clusters
