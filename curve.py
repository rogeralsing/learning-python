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


def curve(x1, y1, x2, y2, x3, y3, x4, y4):
    left = calc_line(x1, y1, x2, y2)
    right = calc_line(x3, y3, x4, y4)
    top = calc_line(x2, y2, x4, y4)

    plt.plot(*zip(*[(x1, y1), (x2, y2), (x4, y4), (x3, y3)]))

    points = []
    for i in range(0, 10 + 1):
        p_left = left[i]
        p_top = top[i]
        p_right = right[10 - i]

        l1 = calc_line(p_left[0], p_left[1], p_top[0], p_top[1])
        p1 = l1[i]
        l2 = calc_line(p_top[0], p_top[1], p_right[0], p_right[1])
        p2 = l2[i]
        l3 = calc_line(p1[0], p1[1], p2[0], p2[1])
        p = l3[i]

        points.append(p)
    plt.plot(*zip(*points))


curve(5, 20,
      0, 30,
      15, 20,
      25, 40)

plt.show()
