import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN


class ClusterPoint:
    def __init__(self, xy):
        self.xy = xy
        self.neighbours = set()
        self.taken = False

    def take(self):
        self.taken = True
        return self


def dbscan(data, max_distance: float = 100, min_pts: int = 2):
    points = get_cluster_points(data, max_distance)

    def scan(cluster):
        for p in cluster:
            cluster += [n.take() for n in p.neighbours if not n.taken]

        return cluster

    return [scan([p.take()]) for p in points if not p.taken and len(p.neighbours) >= min_pts]


def sk_dbscan(data, max_distance: float = 100, min_pts: int = 3):
    points = get_cluster_points(data, max_distance)
    clustering = DBSCAN(eps=max_distance, min_samples=min_pts).fit(np.array(data))
    clusters = [list() for _ in range(max(clustering.labels_) + 1)]

    for i, p in enumerate(points):
        if clustering.labels_[i] != -1:
            c = clusters[clustering.labels_[i]]
            c += [p]

    return clusters


def get_cluster_points(data, max_distance):
    points = [ClusterPoint(p) for p in data]
    tree = cKDTree(data)
    for i, l in enumerate(tree.query_ball_point(data, max_distance)):
        points[i].neighbours = [points[x] for x in l if x != i]
    return points
