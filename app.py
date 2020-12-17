import random
import time
import matplotlib.pyplot as plt

from clustering import dbscan, sk_dbscan, get_pairs, get_minimum_spanning_tree
from plot import plot, plot_tree
from shapes import with_convex_hull, with_unions, with_alpha

points = [(random.randint(0, 1000), random.randint(0, 1000))
          for i in range(120)]

start_time = time.time()
clusters = dbscan(points, 100)
print("Custom --- %s seconds ---" % (time.time() - start_time))
print("%s clusters" % len(clusters))

start_time = time.time()
sk_clusters = sk_dbscan(points, 100)
print("SKLEARN --- %s seconds ---" % (time.time() - start_time))
print("%s clusters" % len(sk_clusters))


pairs = get_pairs(clusters[0])
tree = get_minimum_spanning_tree(pairs)
print(tree)

plot_tree(plt, 'Blue', tree)
plt.show()

fig, ax = plt.subplots(4, 1, constrained_layout=True)
fig.set_figheight(20)

ax[0].set_title("Convex Hull")
ax[0].axis('off')
plot(clusters, with_convex_hull(), ax[0])

ax[1].set_title("Alpha Shape")
ax[1].axis('off')
plot(clusters, with_alpha(), ax[1])

ax[2].set_title("My DBSCAN - Unions")
ax[2].axis('off')
plot(clusters, with_unions(), ax[2])

ax[3].set_title("SK-DBSCAN - Unions")
ax[3].axis('off')
plot(sk_clusters, with_unions(), ax[3])
plt.show()
