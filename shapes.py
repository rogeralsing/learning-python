from functools import reduce

from alphashape import alphashape
from shapely.geometry import Point, MultiPoint


def with_convex_hull(buffer=30, simplify=0):
    def f(c):
        mp = MultiPoint(c)
        hull = mp.convex_hull
        expanded = hull.buffer(buffer)
        simplified = expanded.simplify(simplify)
        return simplified

    return f


def with_unions(tolerance=100, buffer=30, simplify=0):
    def f(c):
        points = list(map(lambda p: Point(*p).buffer(tolerance), c))
        shape = reduce(lambda a, b: a.union(b), points)
        simplified = shape.simplify(10).buffer(-tolerance + buffer / 2).buffer(buffer / 2).simplify(simplify)
        return simplified

    return f


def with_alpha(buffer=30, simplify=0, alpha=0.006):
    def f(c):
        hull = alphashape(c, alpha)
        expanded = hull.buffer(buffer)
        simplified = expanded.simplify(simplify)
        return simplified

    return f
