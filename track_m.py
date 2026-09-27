import torch
import math_functions
import config

device = torch.device(config.DEVICE)

theta = torch.linspace(0, 2 * torch.pi, config.SEGMENT_N // 2 + 1, device=device, dtype=torch.float32)[:-1]
wobble = (30 * torch.sin(3 * theta) + 24 * torch.sin(4.5 * theta))

r_inner = 180 + wobble
r_outer = 300 + wobble

inner_x = r_inner * torch.cos(theta)
inner_y = r_inner * torch.sin(theta)

outer_x = r_outer * torch.cos(theta)
outer_y = r_outer * torch.sin(theta)

inner_x1 = inner_x
inner_y1 = inner_y

inner_x2 = torch.roll(inner_x, -1)
inner_y2 = torch.roll(inner_y, -1)

outer_x1 = outer_x
outer_y1 = outer_y

outer_x2 = torch.roll(outer_x, -1)
outer_y2 = torch.roll(outer_y, -1)

px1 = torch.asarray([173, 0])
py1 = torch.asarray([-50, -226])
px2 = torch.asarray([210, 0])
py2 = torch.asarray([-59, -266])

if config.ADD_DIF:
    render_inner_x1 = torch.cat([inner_x1, px1]).cpu().numpy()
    render_inner_y1 = torch.cat([inner_y1, py1]).cpu().numpy()
    render_inner_x2 = torch.cat([inner_x2, px2]).cpu().numpy()
    render_inner_y2 = torch.cat([inner_y2, py2]).cpu().numpy()
else:
    render_inner_x1 = inner_x1.cpu().numpy()
    render_inner_y1 = inner_y1.cpu().numpy()
    render_inner_x2 = inner_x2.cpu().numpy()
    render_inner_y2 = inner_y2.cpu().numpy()

render_outer_x1 = outer_x1.cpu().numpy()
render_outer_y1 = outer_y1.cpu().numpy()
render_outer_x2 = outer_x2.cpu().numpy()
render_outer_y2 = outer_y2.cpu().numpy()

checkpoints_x1 = torch.cat([inner_x1, inner_x2])
checkpoints_y1 = torch.cat([inner_y1, inner_y2])
checkpoints_x2 = torch.cat([outer_x1, outer_x2])
checkpoints_y2 = torch.cat([outer_y1, outer_y2])

render_checkpoints_x1 = checkpoints_x1.cpu().numpy()
render_checkpoints_y1 = checkpoints_y1.cpu().numpy()
render_checkpoints_x2 = checkpoints_x2.cpu().numpy()
render_checkpoints_y2 = checkpoints_y2.cpu().numpy()


def caclDistance(ox, oy, dx, dy):

    d_i, pxi, pyi = math_functions.ray_segment_intersection(ox, oy, dx, dy, inner_x1, inner_y1, inner_x2, inner_y2)
    d_o, pxo, pyo = math_functions.ray_segment_intersection(ox, oy, dx, dy, outer_x1, outer_y1, outer_x2, outer_y2)

    use_inner = torch.where(
        torch.isnan(d_i),
        torch.zeros_like(d_i, dtype=torch.bool),
        torch.where(
            torch.isnan(d_o),
            torch.ones_like(d_i, dtype=torch.bool),
            d_i < d_o
        )
    )

    dist = torch.where(use_inner, d_i, d_o)
    px = torch.where(use_inner, pxi, pxo)
    py = torch.where(use_inner, pyi, pyo)

    return dist, px, py


def check_collision(cx, cy, r):
    inner_collision = math_functions.circle_segment_intersection(
        inner_x1,
        inner_y1,
        inner_x2 - inner_x1,
        inner_y2 - inner_y1,
        cx,
        cy,
        r
    )
    inner_collision = torch.any(inner_collision, dim=1)

    outer_collision = math_functions.circle_segment_intersection(
        outer_x1,
        outer_y1,
        outer_x2 - outer_x1,
        outer_y2 - outer_y1,
        cx,
        cy,
        r
    )
    outer_collision = torch.any(outer_collision, dim=1)

    if config.ADD_DIF:
        dif_collision = math_functions.circle_segment_intersection(
            px1,
            py1,
            px2 - px1,
            py2 - py1,
            cx,
            cy,
            r
        )
        dif_collision = torch.any(dif_collision, dim=1)
        return inner_collision | outer_collision | dif_collision
    else:
        return inner_collision | outer_collision


def check_checkpoint_collision(cx, cy, r):
    checkpoint_collision = math_functions.circle_segment_intersection(
        checkpoints_x1,
        checkpoints_y1,
        checkpoints_x2 - checkpoints_x1,
        checkpoints_y2 - checkpoints_y1,
        cx,
        cy,
        r
    )

    any_collision = torch.any(checkpoint_collision, dim=1)
    checkpoint_idx = torch.argmax(checkpoint_collision.to(torch.int64), dim=1)
    checkpoint_idx = torch.where(any_collision, checkpoint_idx, torch.full_like(checkpoint_idx, -1))

    return checkpoint_idx