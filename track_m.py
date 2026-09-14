import numpy as np
import math_functions
import math
import config

theta = np.linspace(0, 2 * np.pi, config.SEGMENT_N // 2, endpoint=False)
wobble = 30 * np.sin(3 * theta) + 24 * np.sin(4.5 * theta)

r_inner = 180 + wobble
r_outer = 300 + wobble

inner_x = r_inner * np.cos(theta)
inner_y = r_inner * np.sin(theta)

outer_x = r_outer * np.cos(theta)
outer_y = r_outer * np.sin(theta)

inner_x1, inner_y1 = inner_x, inner_y
inner_x2, inner_y2 = np.roll(inner_x, -1), np.roll(inner_y, -1)

outer_x1, outer_y1 = outer_x, outer_y
outer_x2, outer_y2 = np.roll(outer_x, -1), np.roll(outer_y, -1)


def caclDistance(ox, oy, dx, dy):
    origin = np.array([ox, oy])
    direction = np.array([dx, dy])

    d_i, point_i = math_functions.ray_segment_intersection(origin, direction, inner_x1, inner_y1, inner_x2, inner_y2)
    d_o, point_o = math_functions.ray_segment_intersection(origin, direction, outer_x1, outer_y1, outer_x2, outer_y2)

    if d_i is None and d_o is None:
        return None, None, None
    if d_i is None:
        return d_o, point_o[0], point_o[1]
    if d_o is None:
        return d_i, point_i[0], point_i[1]

    if d_i < d_o:
        return d_i, point_i[0], point_i[1]
    return d_o, point_o[0], point_o[1]