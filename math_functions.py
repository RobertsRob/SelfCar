import numpy as np

def ray_segment_intersection(origin, direction, ax, ay, bx, by):
    ox, oy = origin
    dx, dy = direction

    sx = bx - ax
    sy = by - ay
    denom = dx * sy - dy * sx

    with np.errstate(divide='ignore', invalid='ignore'):
        t = ((ax - ox) * sy - (ay - oy) * sx) / denom
        u = ((ax - ox) * dy - (ay - oy) * dx) / denom

    valid = (
        (denom != 0) &
        (t >= 0) &
        (u >= 0) &
        (u <= 1)
    )

    if not np.any(valid):
        return None, None

    t_valid = t[valid]
    best_index = np.argmin(t_valid)
    best_t = t_valid[best_index]

    px = ox + best_t * dx
    py = oy + best_t * dy

    return best_t, (px, py)