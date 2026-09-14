import pygame
import numpy as np
import track_m


pygame.init()
WIDTH, HEIGHT = (1280, 720)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self Car")
clock = pygame.time.Clock()
running = True

car_x, car_y = (200, 200)
car_dx, car_dy = (-1, -0.2)

def drawLine(segment):
    x1, y1, x2, y2 = segment
    pygame.draw.line(screen, (255, 0, 0), to_screen(x1, y1), to_screen(x2, y2), 2)

def to_screen(x, y):
    return (WIDTH // 2 + x, HEIGHT // 2 - y)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    for i in range(len(track_m.inner_x1)):
        k = 100
        x1, y1 = track_m.inner_x1[i], track_m.inner_y1[i]
        x2, y2 = track_m.inner_x2[i], track_m.inner_y2[i]
        drawLine((x1, y1, x2, y2))
    for i in range(len(track_m.outer_x1)):
        k = 100
        x1, y1 = track_m.outer_x1[i], track_m.outer_y1[i]
        x2, y2 = track_m.outer_x2[i], track_m.outer_y2[i]
        drawLine((x1, y1, x2, y2))

    pygame.draw.circle(screen, (255, 255, 0), to_screen(car_x, car_y), 8)
    d, px, py = track_m.caclDistance(car_x, car_y, car_dx, car_dy)
    drawLine((car_x, car_y, px, py))
    pygame.draw.circle(screen, (100, 255, 100), to_screen(px, py), 6)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
