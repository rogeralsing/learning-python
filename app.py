import random

from clustering import cluster
from plot import plot
from shapes import with_convex_hull, with_unions

points = [(random.randint(0, 1000), random.randint(0, 1000))
          for i in range(100)]

clusters = cluster(points, 100)
print(clusters)
plot(clusters, with_convex_hull())
plot(clusters, with_unions())
