import matplotlib.colors as colors
from descartes import PolygonPatch


def plot(clusters, f, ax):
    palette = [color for name, color in colors.TABLEAU_COLORS.items()]
    for i, c in enumerate(clusters):
        color = palette[i % len(palette)] if len(c) > 1 else "#e0e0e0"

        points = [cp.xy for cp in c]
        polygon = f(points)

        if polygon.is_empty:
            continue

        plot_patch(ax, color, polygon)
        plot_skeleton(ax, color, c)
        plot_points(ax, color, c)


def plot_patch(ax, color, polygon):
    patch = PolygonPatch(polygon, color=color, alpha=0.2)
    ax.add_patch(patch)


def plot_points(plt, color, c):
    sizes = [len(cp.neighbours)*10+5 for cp in c]
    points = [cp.xy for cp in c]
    plt.scatter(*zip(*points), sizes, color='White', edgecolors=color,zorder=10)


def plot_skeleton(plt, color, c):
    for p in c:
        for child in p.neighbours:
            line = [p.xy, child.xy]
            plt.plot(*zip(*line), color=color, alpha=0.5, linewidth=1)
