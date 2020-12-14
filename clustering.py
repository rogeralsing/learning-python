from scipy.spatial import KDTree


class ClusterPoint:
    def __init__(self, xy):
        self.xy = xy
        self.neighbours = set()
        self.taken = False

    def take(self):
        self.taken = True
        return self


def dbscan(data, max_distance: float = 100, min_pts=3):
    points = [ClusterPoint(p) for p in data]

    tree = KDTree(data)
    for i, l in enumerate(tree.query_ball_point(data, max_distance)):
        points[i].neighbours = [points[x] for x in l if x != i]

    def scan(cluster):
        for p in cluster:
            cluster += [n.take() for n in p.neighbours if not n.taken]

        return cluster

    return [scan([p.take()]) for p in points if not p.taken and len(p.neighbours) >= min_pts]
