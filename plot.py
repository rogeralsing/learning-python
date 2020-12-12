import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def plot_poly(plt, poly, color):
    if poly.geom_type == 'MultiPolygon':
        for g in poly.geoms:
            plot_poly(plt, g, color)
    elif poly.geom_type == 'Polygon':
        plt.plot(*poly.exterior.xy, color=color)
        plt.fill(*poly.exterior.xy, alpha=0.2, color=color)
    else:
        pass


def plot(clusters, f):
    palette = [color for name, color in mcolors.TABLEAU_COLORS.items()]
    for i, c in enumerate(clusters):
        points = c.xy()
        plt.scatter(*zip(*points))

        polygon = f(points)

        color = palette[i % len(palette)]
        plot_poly(plt, polygon, color)

    plt.show()
