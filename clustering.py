from scipy.spatial import KDTree


class ClusterPoint:
    def __init__(self, xy):
        self.xy = xy
        self.linked = set()
        self.done = False


def dbscan(points, max_distance: float = 100, min_pts=3):
    cluster_points = [ClusterPoint(p) for p in points]

    # for every point, get every other point within range
    # build ClusterPoints from the resulting data
    tree = KDTree(points)
    for i, l in enumerate(tree.query_ball_point(points, max_distance)):
        cluster_points[i].linked = {cluster_points[x] for x in l if x != i}

    def build_cluster(current_cluster):
        current_cluster[0].done = True
        for current_point in current_cluster:
            for linked_point in current_point.linked:
                if not linked_point.done:
                    current_cluster.append(linked_point)
                    linked_point.done = True

        return current_cluster

    return [build_cluster([cp]) for cp in cluster_points if not cp.done and len(cp.linked) >= min_pts]
