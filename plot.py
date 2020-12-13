import matplotlib.colors as colors
from descartes import PolygonPatch


def plot(clusters, f, ax):
    palette = [color for name, color in colors.TABLEAU_COLORS.items()]
    for i, c in enumerate(clusters):
        color = palette[i % len(palette)] if len(c) > 1 else "#e0e0e0"

        points = c.xy()
        polygon = f(points)

        if not polygon.is_empty:
            patch = PolygonPatch(polygon.buffer(0),color=color, alpha=0.2)
            ax.add_patch(patch)

            plot_skeleton(ax, c, color)
            plot_points(ax, color, points)


def plot_points(plt, color, points):
    plt.scatter(*zip(*points), color=color)


def plot_skeleton(plt, c, color):
    for p in c.skeleton:
        for child in p.linked:
            line = [(p.x, p.y), (child.x, child.y)]
            plt.plot(*zip(*line), color=color, alpha=0.5, linewidth=1)
