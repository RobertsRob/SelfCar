import numpy as np

def ray_segment_intersection(ox, oy, dx, dy, ax, ay, bx, by):
    ox = ox[:, None]
    oy = oy[:, None]
    dx = dx[:, None]
    dy = dy[:, None]

    sx = bx - ax          # (m,)
    sy = by - ay           # (m,)
    denom = dx * sy - dy * sx   # (n, m)

    with np.errstate(divide='ignore', invalid='ignore'):
        t = ((ax - ox) * sy - (ay - oy) * sx) / denom
        u = ((ax - ox) * dy - (ay - oy) * dx) / denom

    valid = (denom != 0) & (t >= 0) & (u >= 0) & (u <= 1)

    t_masked = np.where(valid, t, np.inf)
    best_index = np.argmin(t_masked, axis=1)
    best_t = t_masked[np.arange(t_masked.shape[0]), best_index]

    hit = np.isfinite(best_t)
    best_t = np.where(hit, best_t, np.nan)

    px = np.where(hit, ox[:, 0] + best_t * dx[:, 0], np.nan)
    py = np.where(hit, oy[:, 0] + best_t * dy[:, 0], np.nan)

    return best_t, px, py