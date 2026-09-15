import torch

def ray_segment_intersection(ox, oy, dx, dy, ax, ay, bx, by):

    ox = ox[:, None]
    oy = oy[:, None]
    dx = dx[:, None]
    dy = dy[:, None]

    sx = bx - ax
    sy = by - ay

    denom = dx * sy - dy * sx

    t = torch.where(denom != 0, ((ax - ox) * sy - (ay - oy) * sx) / denom, torch.inf)
    u = torch.where(denom != 0, ((ax - ox) * dy - (ay - oy) * dx) / denom, torch.inf)
    valid = ((denom != 0) & (t >= 0) & (u >= 0) & (u <= 1))
    t_masked = torch.where(valid, t, torch.inf)

    best_index = torch.argmin(t_masked, dim=1)
    best_t = t_masked[torch.arange(t_masked.shape[0], device=ox.device), best_index]

    hit = torch.isfinite(best_t)
    best_t = torch.where(hit, best_t, torch.nan)

    px = torch.where(hit, ox[:, 0] + best_t * dx[:, 0], torch.nan)
    py = torch.where(hit, oy[:, 0] + best_t * dy[:, 0], torch.nan)

    return best_t, px, py