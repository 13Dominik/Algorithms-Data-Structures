# Convex hull algorithm
# Dominik Tomalczyk
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:  # collinear
        return 0
    elif val > 0:  # clockwise
        return 1
    else:  # counterclockwise
        return 2


def left_point(points):
    min_point = 0  # INDEX in list (points) of the left most point
    for i in range(1, len(points)):
        if points[i].x < points[min_point].x:
            min_point = i
        elif points[i].x == points[min_point].x:
            if points[i].y < points[min_point].y:
                min_point = i
    return min_point


def convex_hull(points):
    start = left_point(points)  # point with min x, min y
    hull = []  # points
    p = start  # starting index
    while True:
        hull.append(points[p])  # add current point to list
        q = (p + 1) % len(points)  # start q index
        for r in range(len(points)):
            # if orientatian of p,r,q is counterclockwise: set q to r
            if orientation(points[p], points[r], points[q]) == 2:
                q = r
        # next p is current q
        p = q
        # while we didnt make a loop
        if p == start:
            break

    return hull


def convex_hull_v2(points):
    """
    skip unnecessary points (linear points)
    :param points:
    :return: hull
    """
    start = left_point(points)  # point with min x, min y
    hull = []  # points
    p = start  # starting index
    while True:
        hull.append(points[p])  # add current point to list
        q = (p + 1) % len(points)  # start q index
        for r in range(len(points)):
            # if orientatian of p,r,q is collinear: set q to r
            if orientation(points[p], points[r], points[q]) == 0:
                if points[p].x < points[q].x < points[r].x:
                    q = r
                elif points[p].x == points[q].x == points[r].x and points[p].y < points[q].y < points[r].y:
                    q = r
                elif points[r].x < points[q].x < points[p].x:
                    q = r
                elif points[r].x == points[q].x == points[p].x and points[r].y < points[q].y < points[p].y:
                    q = r
            # if orientatian of p,r,q is counterclockwise: set q to r
            elif orientation(points[p], points[r], points[q]) == 2:
                q = r
        # next p is current q
        p = q
        # while we didnt make a loop
        if p == start:
            break

    return hull


p1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
p2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
p = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
points = []
points1 = []
points2 = []
for point in p:
    points.append(Point(point[0], point[1]))
for point in p1:
    points1.append(Point(point[0], point[1]))
for point in p2:
    points2.append(Point(point[0], point[1]))
print(convex_hull(points))
print(convex_hull_v2(points))
