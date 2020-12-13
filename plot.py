import matplotlib.colors as colors
from descartes import PolygonPatch


def plot(clusters, f, ax):
    palette = [color for name, color in colors.TABLEAU_COLORS.items()]
    for i, c in enumerate(clusters):
        color = palette[i % len(palette)] if len(c) > 1 else "#e0e0e0"

        points = [(cp.x,cp.y) for cp in c]
        polygon = f(points)

        if polygon.is_empty:
            continue

        plot_patch(ax, color, polygon)
        plot_skeleton(ax, color, c)
        plot_points(ax, color, points)


def plot_patch(ax, color, polygon):
    patch = PolygonPatch(polygon, color=color, alpha=0.2)
    ax.add_patch(patch)


def plot_points(plt, color, points):
    plt.scatter(*zip(*points), color=color)


def plot_skeleton(plt, color, c):
    for p in c:
        for child in p.linked:
            line = [(p.x, p.y), (child.x, child.y)]
            plt.plot(*zip(*line), color=color, alpha=0.5, linewidth=1)
