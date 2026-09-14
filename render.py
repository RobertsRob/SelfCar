import pygame
import config
import track_m

def drawLine(screen, segment):
    x1, y1, x2, y2 = segment
    pygame.draw.line(screen, (255, 0, 0), to_screen(x1, y1), to_screen(x2, y2), 2)

def to_screen(x, y):
    return (config.WIDTH // 2 + x, config.HEIGHT // 2 - y)

def drawTrack(screen):
    screen.fill("black")
    for i in range(len(track_m.inner_x1)):
        k = 100
        x1, y1 = track_m.inner_x1[i], track_m.inner_y1[i]
        x2, y2 = track_m.inner_x2[i], track_m.inner_y2[i]
        drawLine(screen, (x1, y1, x2, y2))
    for i in range(len(track_m.outer_x1)):
        k = 100
        x1, y1 = track_m.outer_x1[i], track_m.outer_y1[i]
        x2, y2 = track_m.outer_x2[i], track_m.outer_y2[i]
        drawLine(screen, (x1, y1, x2, y2))

def drawDot(screen, pos, r, color):
    x, y = pos
    pygame.draw.circle(screen, (255, 255, 0), to_screen(x, y), r)
    # d, px, py = track_m.caclDistance(car_x, car_y, car_dx, car_dy)
    # render.drawLine(screen, (car_x, car_y, px, py))
    # pygame.draw.circle(screen, (100, 255, 100), render.to_screen(px, py), 6)