import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN
from funcs import Bag, Node


def dbscan(data, max_distance: float = 100, min_pts: int = 3):
    nodes = get_nodes(data, max_distance)
    clusters = []
    bag = Bag(nodes)
    for root in nodes:
        if len(root.neighbours) >= min_pts and bag.try_take(root):
            cluster = [root]
            clusters.append(cluster)
            for p in cluster:
                cluster.extend([n for n in p.neighbours if bag.try_take(n)])

    return clusters


def sk_dbscan(data, max_distance: float = 100, min_pts: int = 3):
    nodes = get_nodes(data, max_distance)
    clustering = DBSCAN(eps=max_distance, min_samples=min_pts, algorithm='kd_tree').fit(np.array(data))
    clusters = [[] for _ in range(max(clustering.labels_) + 1)]

    for p, l in zip(nodes, clustering.labels_):
        if l != -1:
            clusters[l].append(p)

    return clusters


def get_nodes(data, max_distance):
    points = [Node(p) for p in data]
    tree = cKDTree(data)
    for i, l in enumerate(tree.query_ball_point(data, max_distance)):
        points[i].neighbours = [points[x] for x in l]
    return points
