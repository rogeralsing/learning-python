# https://www.deke.com/content/how-bezier-curves-really-work
import matplotlib.pyplot as plt


def calc_line(x1, y1, x2, y2, steps=10):
    dx = (x2 - x1) / steps
    dy = (y2 - y1) / steps
    res = []

    x = x1
    y = y1
    for _ in range(0, steps + 1):
        res.append((x, y))
        x += dx
        y += dy

    return res


def calc_point(x1, y1, x2, y2, step, steps=10):
    dx = (x2 - x1) / steps
    dy = (y2 - y1) / steps

    x = x1 + dx * step
    y = y1 + dy * step

    return x, y


def curve(x1, y1, x2, y2, x3, y3, x4, y4, steps=10):
    left = calc_line(x1, y1, x2, y2, steps)
    right = calc_line(x3, y3, x4, y4, steps)
    top = calc_line(x2, y2, x4, y4, steps)

    plt.plot(*zip(*[(x1, y1), (x2, y2), (x4, y4), (x3, y3)]))

    points = []
    for i in range(0, steps + 1):
        p_left = left[i]
        p_top = top[i]
        p_right = right[steps - i]

        p1 = calc_point(p_left[0], p_left[1], p_top[0], p_top[1], i, steps)
        p2 = calc_point(p_top[0], p_top[1], p_right[0], p_right[1], i, steps)
        p_final = calc_point(p1[0], p1[1], p2[0], p2[1], i, steps)

        points.append(p_final)
    plt.plot(*zip(*points))


curve(5, 20,
      0, 30,
      15, 20,
      25, 40,
      20)

plt.show()
