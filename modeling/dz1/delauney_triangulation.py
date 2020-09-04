DIRECT = 1  # по часовой
ALIGNED = 0  # на одной линии
INDIRECT = -1  # против часовой

INSIDE = 1  # внутри окружности
CIRCLE = 0  # на окружности
OUTSIDE = -1  # вне окружности


def inv(point):
    x, y = point
    return (y, x)


def orientation(a, b, c):
    xa, ya = a
    xb, yb = b
    xc, yc = c
    # определитель матрицы:
    d = (xb - xa) * (yc - ya) - (yb - ya) * (xc - xa)
    if d > 0:
        return DIRECT
    elif d == 0:
        return ALIGNED
    return INDIRECT


def circle_position(a, b, c, d):

    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d
    m = [[ax - dx, ay - dy, (ax - dx) ** 2 + (ay - dy) ** 2],
         [bx - dx, by - dy, (bx - dx) ** 2 + (by - dy) ** 2],
         [cx - dx, cy - dy, (cx - dx) ** 2 + (cy - dy) ** 2]]
    # определитель матрицы m :
    d = m[0][0] * m[1][1] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1] - \
        m[0][0] * m[1][2] * m[2][1] - m[0][1] * m[1][0] * m[2][2] - m[0][2] * m[1][1] * m[2][0]
    if d > 0:
        return INSIDE
    elif d == 0:
        return CIRCLE
    return OUTSIDE


def count_xy(points):
    n = len(points)
    sum_x, sum_y, sum_sqx, sum_sqy = 0, 0, 0, 0
    for (x, y) in points:
        sum_x += x
        sum_y += y
        sum_sqx += x ** 2
        sum_sqy += y ** 2
    var_x = (sum_sqx / n) - (sum_x / n) ** 2
    var_y = (sum_sqy / n) - (sum_y / n) ** 2
    return var_x, var_y


def median(points, key=None):
    n = len(points)
    points = sorted(points, key=key)
    return points[n // 2]


def median_recursion(points, start, end, key=None, k=7, max=100):
    if end - start <= max:
        return median(points[start:end], key)
    submedians = [median_recursion(points, start + (i * (end - start)) // k,
                                   start + ((i + 1) * (end - start)) // k,
                                   key, k, max)
                  for i in range(k)]
    return median(submedians, key)


def draw_median(l, key=None, k=7, max=100):
    return median_recursion(l, 0, len(l), key, k, max)


def delaunay_triangulation(points):

    succ = {}
    pred = {}
    first = {}

    def delete(a, b):
        sa = succ.pop((a, b))
        sb = succ.pop((b, a))
        pa = pred.pop((a, b))
        pb = pred.pop((b, a))
        succ[a, pa] = sa
        succ[b, pb] = sb
        pred[a, sa] = pa
        pred[b, sb] = pb

    def insert(a, b, sa, pb):
        pa = pred[a, sa]
        sb = succ[b, pb]
        succ[a, pa] = b
        succ[a, b] = sa
        pred[a, sa] = b
        pred[a, b] = pa
        pred[b, sb] = a
        pred[b, a] = pb
        succ[b, pb] = a
        succ[b, a] = sb

    def hull(x0, y0):

        x, y = x0, y0
        z0 = first[y]
        z1 = first[x]
        z2 = pred[x, z1]
        while True:
            if orientation(x, y, z0) == INDIRECT:
                y, z0 = z0, succ[z0, y]
            elif orientation(x, y, z2) == INDIRECT:
                x, z2 = z2, pred[z2, x]
            else:
                return (x, y)

    def merge(x, y):
        insert(x, y, first[x], pred[y, first[y]])
        first[x] = y

        while True:
            if orientation(x, y, pred[y, x]) == DIRECT:
                y1 = pred[y, x]
                y2 = pred[y, y1]
                while circle_position(x, y, y1, y2) == INSIDE:
                    delete(y, y1)
                    y1 = y2
                    y2 = pred[y, y1]
            else:
                y1 = None

            if orientation(x, y, succ[x, y]) == DIRECT:
                x1 = succ[x, y]
                x2 = succ[x, x1]
                while circle_position(x, y, x1, x2) == INSIDE:
                    delete(x, x1)
                    x1 = x2
                    x2 = succ[x, x1]
            else:
                x1 = None

            if x1 is None and y1 is None:
                break
            elif x1 is None:
                # Рисуем  (x, y1)
                insert(y1, x, y, y)
                y = y1
            elif y1 is None:
                # Рисуем (y, x1)
                insert(y, x1, x, x)
                x = x1
            elif circle_position(x, y, y1, x1) == INSIDE:
                insert(y, x1, x, x)
                x = x1
            else:
                insert(y1, x, y, y)
                y = y1

        first[y] = x

    def triangulate(points):
        n = len(points)

        if n == 2:
            # если есть только две точки, рисуем отрезок [a, b]
            [a, b] = points
            succ[a, b] = pred[a, b] = b
            succ[b, a] = pred[b, a] = a
            first[a] = b
            first[b] = a

        elif n == 3:
            [a, b, c] = points

            if orientation(a, b, c) == DIRECT:
                succ[a, c] = succ[c, a] = pred[a, c] = pred[c, a] = b
                succ[a, b] = succ[b, a] = pred[a, b] = pred[b, a] = c
                succ[b, c] = succ[c, b] = pred[b, c] = pred[c, b] = a
                first[a] = b
                first[b] = c
                first[c] = a
            elif orientation(a, b, c) == INDIRECT:
                succ[a, b] = succ[b, a] = pred[a, b] = pred[b, a] = c
                succ[a, c] = succ[c, a] = pred[a, c] = pred[c, a] = b
                succ[b, c] = succ[c, b] = pred[b, c] = pred[c, b] = a
                first[a] = c
                first[b] = a
                first[c] = b
            else:
                [a, b, c] = sorted(points)

                succ[a, b] = pred[a, b] = succ[c, b] = pred[c, b] = b
                succ[b, a] = pred[b, a] = c
                succ[b, c] = pred[b, c] = a
                first[a] = b
                first[c] = b

        else:  # если 4 или больше точки:
            var_x, var_y = count_xy(points)
            if var_y < var_x:
                # Разделяем точки вертикальной линией:
                median = draw_median(points)
                right = [p for p in points if p >= median]
                left = [p for p in points if p < median]
                triangulate(left)
                triangulate(right)
                x, y = hull(max(left), min(right))
                merge(x, y)
            else:
                # Разделяем точки горизонтальной линией:
                median = draw_median(points, key=inv)
                down = [p for p in points if inv(p) < inv(median)]
                up = [p for p in points if inv(p) >= inv(median)]
                triangulate(down)
                triangulate(up)
                x, y = hull(max(down, key=inv), min(up, key=inv))
                merge(x, y)

    triangulate(points)
    return succ
