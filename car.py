import torch
import numpy as np
import render
import track_m
import config

class Cars:
    def __init__(self, n, sx, sy, sdx, sdy, init_speed):
        self.device = torch.device("cuda")
        self.n = n
        self.x = torch.full((n,), sx, dtype=torch.float32, device=self.device)
        self.y = torch.full((n,), sy, dtype=torch.float32, device=self.device)
        self.dx = torch.full((n,), sdx, dtype=torch.float32, device=self.device)
        self.dy = torch.full((n,), sdy, dtype=torch.float32, device=self.device)
        self.v = torch.full((n,), init_speed, dtype=torch.float32, device=self.device)
        self.main_sensor_length = config.MAIN_SENSOR_LENGTH
        self.side_sensor_length = config.SIDE_SENSOR_LENGTH
        self.alive = torch.ones(self.n, dtype=torch.bool, device=self.device)
        self.points = torch.full((n,), 0, dtype=torch.float32, device=self.device)
        self.prev_checkpoint_id = torch.full((n,), 0, dtype=torch.float32, device=self.device)
        self.prev_wrong_checkpoint_id = torch.full((n,), 0, dtype=torch.float32, device=self.device)
        
    def update(self, screen, dt):

        # Pos update  ---------------
        self.x += self.dx * self.v * dt
        self.y += self.dy * self.v * dt

        # Sensor math ---------------
        d, px, py = track_m.caclDistance(self.x, self.y, self.dx, self.dy)
        rpx, rpy = self.dx * self.main_sensor_length + self.x, self.dy * self.main_sensor_length + self.y
        lookAngle = self.directionToAngle(self.dx, self.dy)
        dxr, dyr = self.angleToDirectrion(lookAngle + np.deg2rad(-45))
        dxl, dyl = self.angleToDirectrion(lookAngle + np.deg2rad(45))
        dr, pxr, pyr = track_m.caclDistance(self.x, self.y, dxr, dyr)
        dl, pxl, pyl = track_m.caclDistance(self.x, self.y, dxl, dyl)
        lpxr, lpyr = dxr * self.side_sensor_length + self.x, dyr * self.side_sensor_length + self.y
        lpxl, lpyl = dxl * self.side_sensor_length + self.x, dyl * self.side_sensor_length + self.y

        collision = track_m.check_collision(self.x, self.y, config.CAR_R)
        self.points = torch.where(collision, self.points - 1000, self.points)
        self.alive &= ~collision

        checkpoint_id = track_m.check_checkpoint_collision(self.x, self.y, config.CAR_R)
        self.crossedCheckpoint(checkpoint_id)

        # Render ---------------
        display_data = torch.stack([self.x[0], self.y[0], rpx[0], rpy[0], lpxr[0], lpyr[0], lpxl[0], lpyl[0], px[0], py[0], pxr[0], pyr[0], pxl[0], pyl[0]]).detach().cpu().numpy()
        (x, y, rx, ry, lrx, lry, llx, lly, hit_x, hit_y, hit_rx, hit_ry, hit_lx, hit_ly) = display_data
        points_data = self.points[0].detach().cpu().numpy()

        render.drawLine(screen, (x, y, rx, ry), (0, 255, 0))
        render.drawLine(screen, (x, y, lrx, lry), (0, 255, 0))
        render.drawLine(screen, (x, y, llx, lly), (0, 255, 0))

        render.drawDot(screen, (rx, ry), 3, (0, 0, 255))
        render.drawDot(screen, (lrx, lry), 3, (0, 0, 255))
        render.drawDot(screen, (llx, lly), 3, (0, 0, 255))

        render.drawDot(screen, (hit_x, hit_y), 6, (255, 255, 255))
        render.drawDot(screen, (hit_rx, hit_ry), 6, (255, 255, 255))
        render.drawDot(screen, (hit_lx, hit_ly), 6, (255, 255, 255))

        render.drawDot(screen, (x, y), config.CAR_R, (255, 0, 0))
        render.drawText(screen, "p: " + str(points_data), 20, 40)


    def angleToDirectrion(self, angle):
        dx = torch.cos(angle)
        dy = torch.sin(angle)
        return dx, dy
    
    def directionToAngle(self, dx, dy):
        return torch.atan2(dy, dx)

    def steerAll(self, deg, dt):
        angle = self.directionToAngle(self.dx, self.dy)
        angle += torch.deg2rad(
            torch.tensor(deg * dt, device=self.device)
        )
        self.dx, self.dy = self.angleToDirectrion(angle)

    
    def crossedCheckpoint(self, checkpoint_id):
        max_checkpoint = config.SEGMENT_N // 2 - 1

        no_collision = checkpoint_id == -1
        lap_completed = (~no_collision) & (self.prev_checkpoint_id == max_checkpoint) & (checkpoint_id == 0)
        same = (~no_collision) & (~lap_completed) & (checkpoint_id == self.prev_checkpoint_id)
        advanced = (~no_collision) & (~lap_completed) & (checkpoint_id > self.prev_checkpoint_id)
        regressed_raw = (~no_collision) & (~lap_completed) & (checkpoint_id < self.prev_checkpoint_id)
        is_new_wrong = (self.prev_wrong_checkpoint_id == -1) | (checkpoint_id < self.prev_wrong_checkpoint_id)

        regressed = regressed_raw & is_new_wrong
        returning = regressed_raw & (~is_new_wrong)

        self.prev_checkpoint_id = torch.where(lap_completed | advanced, checkpoint_id, self.prev_checkpoint_id)
        self.prev_wrong_checkpoint_id = torch.where(regressed, checkpoint_id, self.prev_wrong_checkpoint_id)

        self.prev_wrong_checkpoint_id = torch.where(
            lap_completed | advanced,
            torch.full_like(self.prev_wrong_checkpoint_id, -1),
            self.prev_wrong_checkpoint_id
        )

        delta = torch.zeros_like(self.points)
        delta = torch.where(advanced, torch.full_like(self.points, 1.0), delta)
        delta = torch.where(lap_completed, torch.full_like(self.points, 1.0), delta)
        delta = torch.where(regressed, torch.full_like(self.points, -1.0), delta)
        # returning stays at delta = 0, same as no_collision/same

        self.points += delta