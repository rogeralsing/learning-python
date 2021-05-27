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
    plt.scatter(*zip(*left), color="blue")
    plt.scatter(*zip(*right), color="blue")
    plt.scatter(*zip(*top), color="blue")

    for i in range(0, 10 + 1):
        pLeft = left[i]
        pTop = top[i]
        pRight = right[10 - i]

        line = [pLeft, pTop]
        plt.plot(*zip(*line), color="orange")

        line = [pTop, pRight]
        plt.plot(*zip(*line), color="orange")

        l1 = calc_line(pLeft[0], pLeft[1], pTop[0], pTop[1])
        p5 = l1[i]
        l2 = calc_line(pTop[0], pTop[1], pRight[0], pRight[1])
        p6 = l2[i]
        line = [p5, p6]
        plt.plot(*zip(*line), color="green")

        l3 = calc_line(p5[0], p5[1], p6[0], p6[1])
        p = l3[i]
        plt.scatter(*zip(*[p]), [100], color="red")

curve(5, 20,
      0, 30,
      15, 20,
      20, 35)

plt.show()
