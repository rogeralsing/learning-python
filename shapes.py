from functools import reduce

from alphashape import alphashape
from shapely.geometry import Point, MultiPoint


def with_convex_hull(buffer: float = 30, simplify: float = 0):
    def f(c):
        return (MultiPoint(c)
                .convex_hull
                .buffer(buffer)
                .simplify(simplify))

    return f


def with_unions(tolerance: float = 100, buffer: float = 30, simplify: float = 0):
    def f(c):
        points = [Point(*p).buffer(tolerance) for p in c]
        return (reduce(lambda a, b: a.union(b), points)
                .simplify(10)
                .buffer(-tolerance + buffer / 2)
                .buffer(buffer / 2)
                .simplify(simplify))

    return f


def with_alpha(buffer: float = 30, simplify: float = 0, alpha: float = 0.006):
    def f(c):
        return (alphashape(c, alpha)
                .buffer(buffer)
                .simplify(simplify))

    return f
