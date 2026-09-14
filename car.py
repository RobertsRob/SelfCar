import numpy as np
import render

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
        pass