from scipy.spatial import KDTree


class ClusterPoint:
    def __init__(self, xy):
        self.xy = xy
        self.linked = set()
        self.done = False


def cluster(points, max_distance: float = 100):
    cluster_points = [ClusterPoint(p) for p in points]

    # for every point, get every other point within range
    # build ClusterPoints from the resulting data
    tree = KDTree(points)
    for i, l in enumerate(tree.query_ball_point(points, max_distance)):
        cluster_points[i].linked = {cluster_points[x] for x in l if x != i}

    def recurse(current_point: ClusterPoint, current_cluster):
        if current_point.done:
            return

        current_cluster.append(current_point)
        current_point.done = True

        for linked_point in current_point.linked:
            recurse(linked_point, current_cluster)

        return current_cluster

    return [recurse(cp, []) for cp in cluster_points if not cp.done]
