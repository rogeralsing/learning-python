from functools import reduce

from shapely.geometry import Point, MultiPoint


def with_convex_hull(buffer=30, simplify=10):
    def f(c):
        mp = MultiPoint(c)
        hull = mp.convex_hull
        expanded = hull.buffer(buffer)
        simplified = expanded.simplify(simplify)
        return simplified

    return f


def with_unions(buffer=100, shrink=-70, simplify=10):
    def f(c):
        points = list(map(lambda p: Point(*p).buffer(buffer), c))
        shape = reduce(lambda a, b: a.union(b), points)
        simplified = shape.buffer(shrink).simplify(simplify)
        return simplified

    return f
