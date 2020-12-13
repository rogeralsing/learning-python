from typing import Set

from scipy.spatial import KDTree


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
    cluster_points = [ClusterPoint(*p) for p in points]
    tree = KDTree(points)
    links = tree.query_ball_point(points, max_distance)

    def recurse(index: int, current_cluster: Cluster):
        current_point = cluster_points[index]
        current_point.done = True
        current_cluster.add_point(current_point)

        for other_index in links[index]:
            other_point = cluster_points[other_index]
            current_point.link(other_point)

            if other_point.done:
                continue

            recurse(other_index, current_cluster)

        return current_cluster

    return [recurse(i, Cluster()) for i, cp in enumerate(cluster_points)
            if not cp.done]
