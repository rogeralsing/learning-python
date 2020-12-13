import random

import matplotlib.pyplot as plt

from clustering import cluster
from plot import plot
from shapes import with_convex_hull, with_unions, with_alpha

points = [(random.randint(0, 1000), random.randint(0, 1000))
          for i in range(150)]

clusters = cluster(points, 100)

fig, ax = plt.subplots(3, 1, constrained_layout=True)
fig.set_figheight(15)
ax[0].set_title("Convex Hull")
ax[0].axis('off')
plot(clusters, with_convex_hull(), ax[0])

ax[1].set_title("Alpha Shape")
ax[1].axis('off')
plot(clusters, with_alpha(), ax[1])

ax[2].set_title("Unions")
ax[2].axis('off')
plot(clusters, with_unions(), ax[2])
plt.show()
