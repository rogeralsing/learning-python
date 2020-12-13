from scipy.spatial import KDTree


class ClusterPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.linked = set()

    def unlink(self):
        for child in self.linked:
            child.linked.remove(self)
        self.linked.clear()

    def __len__(self):
        return len(self.linked)


def cluster(points, max_distance: float = 100):
    cluster_points = [ClusterPoint(*p) for p in points]
    tree = KDTree(points)
    for i, l in enumerate(tree.query_ball_point(points, max_distance)):
        cluster_points[i].linked = {cluster_points[x] for x in l if x != i}

    remaining_points = set(cluster_points)

    def recurse(current_point: ClusterPoint, current_cluster):
        if current_point not in remaining_points:
            return

        current_cluster.append(current_point)
        remaining_points.remove(current_point)

        for other_point in current_point.linked:
            recurse(other_point, current_cluster)

        return current_cluster

    return [recurse(cp, []) for cp in cluster_points if cp in remaining_points]