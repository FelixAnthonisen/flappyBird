def point_in_rectangle(x0, y0, x1, y1, x2, y2):
    inside_horisontal = x2 >= min(x0, x1) and x2 <= max(x0, x1)
    inside_vertical = y2 >= min(y0, y1) and y2 <= max(y0, y1)
    return inside_vertical and inside_horisontal


def distance_between_points(x0, y0, x1, y1):
    return ((abs(x0 - x1)) ** 2 + (abs(y0 - y1)) ** 2) ** (1 / 2)


def circle_overlaps_rectangle(x0, y0, x1, y1, x2, y2, r):
    top, right, bottom, left = (min(y0, y1), max(x0, x1), max(y0, y1), min(x0, x1))
    if point_in_rectangle(x0, y0, x1, y1, x2, y2):
        return True
    if not point_in_rectangle(left - r, top - r, right + r, bottom + r, x2, y2):
        return False
    if (x2 >= left and x2 <= right) or (y2 >= top and y2 < bottom):
        return True
    return (
        distance_between_points(x2, y2, x0, y0) < r
        or distance_between_points(x2, y2, x1, y0) < r
        or distance_between_points(x2, y2, x0, y1) < r
        or distance_between_points(x2, y2, x1, y1) < r
    )


def is_colliding(obj1, obj2):
    """obj1 has to be a rectangle and obj2 has to be a circle"""
    x0, y0, x1, y1 = (
        obj1.x_pos,
        obj1.y_pos,
        obj1.x_pos + obj1.width,
        obj1.y_pos + obj1.height,
    )
    x2, y2, r = (obj2.centre[0], obj2.centre[1], obj2.radius)
    return circle_overlaps_rectangle(x0, y0, x1, y1, x2, y2, r)
