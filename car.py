import numpy as np
import render
import track_m
import config

class Cars:
    def __init__(self, n, sx, sy, sdx, sdy, init_speed):
        self.n = n
        self.x = np.full(n, sx, dtype=float)
        self.y = np.full(n, sy, dtype=float)
        self.dx = np.full(n, sdx, dtype=float)
        self.dy = np.full(n, sdy, dtype=float)
        self.v = np.full(n, init_speed, dtype=float)
        self.main_sensor_length = config.MAIN_SENSOR_LENGTH
        self.side_sensor_length = config.SIDE_SENSOR_LENGTH
        
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

        # Render ---------------
        render.drawLine(screen, (self.x[0], self.y[0], rpx[0], rpy[0]), (0, 255, 0))
        render.drawLine(screen, (self.x[0], self.y[0], lpxr[0], lpyr[0]), (0, 255, 0))
        render.drawLine(screen, (self.x[0], self.y[0], lpxl[0], lpyl[0]), (0, 255, 0))

        render.drawDot(screen, (rpx[0], rpy[0]), 3, (0, 0, 255))
        render.drawDot(screen, (lpxr[0], lpyr[0]), 3, (0, 0, 255))
        render.drawDot(screen, (lpxl[0], lpyl[0]), 3, (0, 0, 255))

        render.drawDot(screen, (px[0], py[0]), 6, (255, 255, 255))
        render.drawDot(screen, (pxr[0], pyr[0]), 6, (255, 255, 255))
        render.drawDot(screen, (pxl[0], pyl[0]), 6, (255, 255, 255))

        render.drawDot(screen, (self.x[0], self.y[0]), 8, (255, 0, 0))

    def angleToDirectrion(self, angle):
        dx = np.cos(angle)
        dy = np.sin(angle)
        return dx, dy
    
    def directionToAngle(self, dx, dy):
        return np.arctan2(dy, dx)

    def steerAll(self, deg, dt):
        self.dx, self.dy = self.angleToDirectrion(self.directionToAngle(self.dx, self.dy) + np.deg2rad(deg * dt))

    
        