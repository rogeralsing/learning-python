from math import hypot


def cluster(points, d=100):

    def dist(p1, p2):
        return hypot(p1[0] - p2[0], p1[1] - p2[1])

    def recurse(p, bag, c):
        bag.remove(p)
        c.append(p)

        for m in filter(lambda p2: dist(p, p2) < d, bag):
            recurse(m, bag, c)

    clusters = []
    while len(points) > 0:
        p = points[0]
        c = []
        clusters.append(c)
        recurse(p, points, c)
    return clusters