# https://www.deke.com/content/how-bezier-curves-really-work
import matplotlib.pyplot as plt


def calc_point(p1, p2, step, steps=10):
    (x1, y1), (x2, y2) = p1, p2
    x = x1 + (x2 - x1) / steps * step
    y = y1 + (y2 - y1) / steps * step

    return x, y


def curve(p1, p2, p3, p4, steps=10):
    plt.plot(*zip(*[p1, p2, p4, p3]))

    points = [calc_point(
        calc_point(calc_point(p1, p2, i, steps), calc_point(p2, p4, i, steps), i, steps),
        calc_point(calc_point(p2, p4, i, steps), calc_point(p4, p3, i, steps), i, steps),
        i, steps) for i in range(0, steps + 1)]

    plt.plot(*zip(*points))


curve((5, 20), (0, 30), (15, 20), (25, 40), 20)

plt.show()
