from math import hypot

import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN


class Node:
    def __init__(self, xy):
        self.xy = tuple(xy)
        self.neighbours = set()


class Bag:
    def __init__(self, data):
        self.set = set(data)

    def try_take(self, item):
        exists = item in self.set
        self.set.discard(item)
        return exists


def dist(p1, p2):
    return hypot(p1[0] - p2[0], p1[1] - p2[1])


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
    cluster_count = max(clustering.labels_) + 1
    clusters = [[] for _ in range(cluster_count)]

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


def get_pairs(nodes):
    pairs = set()

    for p1 in nodes:
        for p2 in p1.neighbours:
            d = dist(p1.xy, p2.xy)

            pairs.add((p1.xy, p2.xy, d))
            pairs.discard((p2.xy, p1.xy, d))

    return pairs


def get_minimum_spanning_tree(pairs):

    # pair is:
    # ((x1,y1), (x2,y2), distance)

    sorted_pairs = sorted(pairs, key=lambda p: p[2])

    graphs = {}
    l = []
    for pair in sorted_pairs:
        (p1, p2, _) = pair
        g1 = graphs.get(p1)
        g2 = graphs.get(p2)

        if g1 is None or g2 is None:
            g = g1 or g2
            if g is None:
                g = len(l)
                l.append([])

            graphs[p1] = g
            graphs[p2] = g
            l[g].append(pair)

        # p1 and p2 are part of different graphs
        # merge g2 with g1
        elif g1 != g2:
            # merge graphs
            l[g1].extend(l[g2] + [pair])
            for pp1, pp2, _ in l[g2]:
                graphs[pp1] = g1
                graphs[pp2] = g1

            l[g2] = []

    return [x for x in l if len(x) > 0]
