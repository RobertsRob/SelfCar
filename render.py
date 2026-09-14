import pygame
import config
import track_m

def drawLine(screen, segment, color=(255, 0, 0)):
    x1, y1, x2, y2 = segment
    if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
        pygame.draw.line(screen, color, to_screen(x1, y1), to_screen(x2, y2), 2)

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

def drawDot(screen, pos, r, color=(255, 0, 0)):
    x, y = pos
    if x is not None and y is not None:
        pygame.draw.circle(screen, color, to_screen(x, y), r)