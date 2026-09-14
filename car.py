import numpy as np
import render
import track_m

class Cars:
    def __init__(self, n, sx, sy, sdx, sdy, init_speed):
        self.n = n
        self.x = np.full(n, sx)
        self.y = np.full(n, sy)
        self.dx = np.full(n, sdx)
        self.dy = np.full(n, sdy)
        self.v = np.full(n, init_speed)
        
    def update(self, screen):
        for i in range(self.n):
            render.drawDot(screen, (self.x[i], self.y[i]), 8, (255, 255, 0))
            d, px, py = track_m.caclDistance(self.x[i], self.y[i], self.dx[i], self.dy[i])
            render.drawLine(screen, (self.x[i], self.y[i], px, py))
            render.drawDot(screen, (px, py), 6, (100, 255, 100))

    def angleToDirectrion(self, angle):
        dx = np.cos(angle)
        dy = np.sin(angle)
        return dx, dy
        