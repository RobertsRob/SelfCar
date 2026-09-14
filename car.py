import numpy as np
import render
import track_m
import config

class Cars:
    def __init__(self, n, sx, sy, sdx, sdy, init_speed):
        self.n = n
        self.x = np.full(n, sx)
        self.y = np.full(n, sy)
        self.dx = np.full(n, sdx)
        self.dy = np.full(n, sdy)
        self.v = np.full(n, init_speed)
        self.side_sensor_length = config.SIDE_SENDOR_LENGTH
        
    def update(self, screen):
        d, px, py = track_m.caclDistance(self.x, self.y, self.dx, self.dy)
        lookAngle = self.directionToAngle(self.dx, self.dy)
        dxr, dyr = self.angleToDirectrion(lookAngle + np.deg2rad(-45))
        dxl, dyl = self.angleToDirectrion(lookAngle + np.deg2rad(45))
        dr, pxr, pyr = track_m.caclDistance(self.x, self.y, dxr, dyr)
        dl, pxl, pyl = track_m.caclDistance(self.x, self.y, dxl, dyl)
        lpxr, lpyr = dxr * self.sensor_length + self.x, dyr * self.sensor_length + self.y
        lpxl, lpyl = dxl * self.sensor_length + self.x, dyl * self.sensor_length + self.y

        for i in range(self.n):
            render.drawDot(screen, (self.x[i], self.y[i]), 8, (255, 255, 0))
            # print(self.x[i], self.y[i], px[i], py[i])
            render.drawLine(screen, (self.x[i], self.y[i], px[i], py[i]), (0, 255, 0))
            render.drawDot(screen, (px[i], py[i]), 6, (100, 255, 100))
            render.drawLine(screen, (self.x[i], self.y[i], lpxr[i], lpyr[i]), (0, 255, 0))
            render.drawLine(screen, (self.x[i], self.y[i], lpxl[i], lpyl[i]), (0, 255, 0))
            render.drawDot(screen, (pxr[i], pyr[i]), 6, (100, 255, 100))
            render.drawDot(screen, (pxl[i], pyl[i]), 6, (100, 255, 100))

    def angleToDirectrion(self, angle):
        dx = np.cos(angle)
        dy = np.sin(angle)
        return dx, dy
    
    def directionToAngle(self, dx, dy):
        return np.arctan2(dy, dx)
        