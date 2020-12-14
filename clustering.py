from scipy.spatial import KDTree


class ClusterPoint:
    def __init__(self, xy):
        self.xy = xy
        self.neighbours = set()
        self.taken = False

    def take(self):
        self.taken = True
        return self


def dbscan(points, max_distance: float = 100, min_pts=3):
    cluster_points = [ClusterPoint(p) for p in points]

    # for every point, get every other point within range
    # build ClusterPoints from the resulting data
    tree = KDTree(points)
    for i, l in enumerate(tree.query_ball_point(points, max_distance)):
        cluster_points[i].neighbours = {cluster_points[x] for x in l if x != i}

    def scan(cluster):
        for p in cluster:
            cluster.extend([n.take() for n in p.neighbours if not n.taken])

        return cluster

    return [scan([p.take()]) for p in cluster_points if not p.taken and len(p.neighbours) >= min_pts]
