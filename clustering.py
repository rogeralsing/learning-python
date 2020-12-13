from math import hypot
from typing import List, Set


class ClusterPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.linked = set()
        self.done = False

    def link(self, other):
        self.linked.add(other)
        other.linked.add(self)

    def unlink(self):
        for child in self.linked:
            child.linked.remove(self)
        self.linked.clear()

    def dist(self, other) -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def in_range(self, other, max_dist):
        return self.dist(other) < max_dist

    def __len__(self):
        return len(self.linked)


class Cluster:
    def __init__(self):
        self.skeleton = []

    def __len__(self):
        return len(self.skeleton)

    def xy(self):
        return [(cp.x, cp.y) for cp in self.skeleton]

    def add_point(self, cp: ClusterPoint):
        self.skeleton.append(cp)

    def erode(self, links=1):
        points: Set[ClusterPoint] = set(self.skeleton)

        done = False
        while not done:
            done = True
            for p in list(points):
                if len(p) <= links:
                    points.remove(p)
                    p.unlink()
                    done = False

        self.skeleton = points
        return self


def cluster(points, max_distance: float = 100):
    def recurse(point: ClusterPoint, bag: Set[ClusterPoint], cluster: Cluster):
        point.done = True
        cluster.add_point(point)

        close_points = [other for other in bag if point.in_range(other, max_distance)]

        for close_point in close_points:
            point.link(close_point)

            if close_point.done:
                continue

            bag.remove(close_point)

            recurse(close_point, bag, cluster)

    clusters: List[Cluster] = []

    ps: Set[ClusterPoint] = {ClusterPoint(x, y) for (x, y) in points}
    while len(ps) > 0:
        p = ps.pop()
        c = Cluster()
        clusters.append(c)
        recurse(p, ps, c)
    return clusters
