import torch
import numpy as np
import render
import track_m
import config
import car_net

class Cars:
    def __init__(self, n, sx, sy, sdx, sdy, init_speed, base_model=None):
        self.device = torch.device("cuda")
        self.n = n
        self.ri = 0
        self.x = torch.full((n,), sx, dtype=torch.float32, device=self.device)
        self.y = torch.full((n,), sy, dtype=torch.float32, device=self.device)
        self.dx = torch.full((n,), sdx, dtype=torch.float32, device=self.device)
        self.dy = torch.full((n,), sdy, dtype=torch.float32, device=self.device)
        self.v = torch.full((n,), init_speed, dtype=torch.float32, device=self.device)
        self.main_sensor_length = config.MAIN_SENSOR_LENGTH
        self.side_sensor_length = config.SIDE_SENSOR_LENGTH
        self.alive = torch.ones(self.n, dtype=torch.bool, device=self.device)
        self.points = torch.full((n,), 0, dtype=torch.float32, device=self.device)
        self.prev_checkpoint_id = torch.zeros(n, dtype=torch.long, device=self.device)
        self.prev_wrong_checkpoint_id = torch.zeros(n, dtype=torch.long, device=self.device)
        self.reward = torch.zeros(self.n, dtype=torch.float32, device=self.device)
        self.lap_count = torch.zeros(self.n, dtype=torch.float32, device=self.device)

        self.models = []

        for i in range(n):
            model = car_net.CarNet().to(self.device)
            if base_model is not None:
                model.load_state_dict(base_model)
                if i != 0:
                    with torch.no_grad():
                        for param in model.parameters():
                            param += torch.randn_like(param) * config.MUTATION_STRENGTH

            self.models.append(model)
        
    def update(self, screen, dt, updates_from_start, time_from_start):
        self.reward = torch.zeros(self.n, dtype=torch.float32, device=self.device)

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
        self.points = torch.where(collision, self.points - 10, self.points)
        self.reward = torch.where(collision, self.reward - 10, self.reward)
        self.alive &= ~collision

        checkpoint_id = track_m.check_checkpoint_collision(self.x, self.y, config.CAR_R)
        checkpoint_id = torch.where(self.alive, checkpoint_id, torch.full_like(checkpoint_id, -1))
        self.crossedCheckpoint(checkpoint_id, updates_from_start, time_from_start)

        # Neural network
        observations = torch.stack([
            torch.clamp(d, 0.0, self.main_sensor_length) / self.main_sensor_length,
            torch.clamp(dr, 0.0, self.side_sensor_length) / self.side_sensor_length,
            torch.clamp(dl, 0.0, self.side_sensor_length) / self.side_sensor_length,
            # self.dx,
            # self.dy
        ], dim=1)

        actions = torch.zeros((self.n, 2), device=self.device)

        for i in range(self.n):
            if self.alive[i].item():
                actions[i] = self.models[i](observations[i:i+1])[0]

        steering = actions[:, 0]
        self.steerAll(steering, dt)

        # Pos update  ---------------
        if config.DT_ON:
            self.x = torch.where(self.alive, self.x + self.dx * self.v * dt, self.x)
            self.y = torch.where(self.alive, self.y + self.dy * self.v * dt, self.y)
        else:
            self.x = torch.where(self.alive, self.x + self.dx * self.v * config.OFF_DT_CONST, self.x)
            self.y = torch.where(self.alive, self.y + self.dy * self.v * config.OFF_DT_CONST, self.y)

        # Render ---------------

        alive_indices = torch.where(self.alive)[0]
        
        for i in alive_indices:
            x = self.x[i].item()
            y = self.y[i].item()
            render.drawDot(screen, (x, y), config.CAR_R, (255, 0, 0))
            render.drawDot(screen, (x, y), config.CAR_R - 0.3, (0, 0, 100))

        alive_points = torch.where(self.alive, self.points, torch.tensor(float("-inf"), device=self.points.device))
        self.ri = torch.argmax(alive_points).item()
        
        display_data = torch.stack([self.x[self.ri], self.y[self.ri], rpx[self.ri], rpy[self.ri], lpxr[self.ri], lpyr[self.ri], lpxl[self.ri], lpyl[self.ri], px[self.ri], py[self.ri], pxr[self.ri], pyr[self.ri], pxl[self.ri], pyl[self.ri]]).detach().cpu().numpy()
        (x, y, rx, ry, lrx, lry, llx, lly, hit_x, hit_y, hit_rx, hit_ry, hit_lx, hit_ly) = display_data
        points_data = self.points[self.ri].detach().cpu().numpy()

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
        render.drawText(screen, "points: " + str(round(float(points_data), 1)), 20, 45)

        

    def angleToDirectrion(self, angle):
        dx = torch.cos(angle)
        dy = torch.sin(angle)
        return dx, dy
    
    def directionToAngle(self, dx, dy):
        return torch.atan2(dy, dx)


    def steerAll(self, steering, dt):
        angle = self.directionToAngle(self.dx, self.dy)
        if config.DT_ON:
            angle += torch.deg2rad(steering * config.ROT_SPEED) * dt
        else:
            angle += torch.deg2rad(steering * config.ROT_SPEED) * config.OFF_DT_CONST
        self.dx, self.dy = self.angleToDirectrion(angle)

    
    def crossedCheckpoint(self, checkpoint_id, updates_from_start, time_from_start):
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
        if config.DT_ON:
            delta = torch.where(lap_completed, config.LAP_AMOUNT_UPDATES / (time_from_start + 1), delta)
        else:
            delta = torch.where(lap_completed, config.LAP_AMOUNT_UPDATES / (updates_from_start + 1), delta)
        delta = torch.where(regressed, torch.full_like(self.points, -1.0), delta)

        self.lap_count += lap_completed.to(self.lap_count.dtype)

        self.points += delta
        self.reward += delta

        self.alive &= self.lap_count < config.LAP_AMOUNT

    def reset(self):
        self.x.fill_(config.SX)
        self.y.fill_(config.SY)

        self.dx.fill_(config.SDX)
        self.dy.fill_(config.SDY)

        self.v.fill_(config.INIT_SPEED)

        self.alive.fill_(True)
        self.points.zero_()
        self.reward.zero_()

        self.prev_checkpoint_id.fill_(0)
        self.prev_wrong_checkpoint_id.fill_(0)
        self.lap_count.fill_(0)