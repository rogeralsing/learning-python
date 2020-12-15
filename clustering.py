from functools import reduce

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


def dbscan(data, max_distance: float = 100, min_pts: int = 3):
    points = get_cluster_points(data, max_distance)
    clusters = []
    for root in points:
        if not root.taken and len(root.neighbours) >= min_pts:
            cluster = [root.take()]
            for p in cluster:
                cluster += [n.take() for n in p.neighbours if not n.taken]
            clusters.append(cluster)

    return clusters


def sk_dbscan(data, max_distance: float = 100, min_pts: int = 3):
    points = get_cluster_points(data, max_distance)
    clustering = DBSCAN(eps=max_distance, min_samples=min_pts, algorithm='kd_tree').fit(np.array(data))
    clusters = [[] for _ in range(max(clustering.labels_) + 1)]

    for p, l in zip(points, clustering.labels_):
        if l != -1:
            clusters[l].append(p)

    return clusters


def get_cluster_points(data, max_distance):
    points = [ClusterPoint(p) for p in data]
    tree = cKDTree(data)
    for i, l in enumerate(tree.query_ball_point(data, max_distance)):
        points[i].neighbours = [points[x] for x in l]
    return points
