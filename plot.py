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
        color = palette[i % len(palette)] if len(c) > 1 else "#e0e0e0"

        points = c.xy()
        polygon = f(points)

        plot_poly(plt, polygon, color)
        plot_skeleton(c, color)
        plot_points(color, points)

    plt.show()


def plot_points(color, points):
    plt.scatter(*zip(*points), color=color)


def plot_skeleton(c, color):
    for p in c.skeleton:
        for child in p.linked:
            line = [(p.x, p.y), (child.x, child.y)]
            plt.plot(*zip(*line), color=color, alpha=0.5, linewidth=1)
