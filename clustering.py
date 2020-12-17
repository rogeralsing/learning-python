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
    sorted_pairs = sorted(pairs, key=lambda p: p[2])

    graphs = {}
    l = []
    g = 0
    for pair in sorted_pairs:
        (p1, p2, _) = pair
        g1 = graphs.get(p1)
        g2 = graphs.get(p2)

        # none of the points are part of a graph
        # create a new graph with id "g"
        if g1 is None and g2 is None:
            graphs[p1] = g
            graphs[p2] = g
            l.append([pair])
            g += 1

        # p1 is not part of a graph, p2 is
        # assign p1 to the same graph as p2
        elif g1 is None:
            graphs[p1] = g2
            l[g2].append(pair)

        # same as above but reverse
        elif g2 is None:
            graphs[p2] = g1
            l[g1].append(pair)

        # p1 and p2 are part of different graphs
        # merge g2 with g1
        elif g1 != g2:
            # merge graphs
            l1 = l[g1]
            l2 = l[g2]
            l1.append(pair)
            l1.extend(l2)
            for p3 in l2:
                graphs[p3] = g1

            l2.clear()

        # both p1 and p2 are already part of the same graph, ignore
        elif g1 == g2:
            pass

    return [x for x in l if len(x) > 0]


