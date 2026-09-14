import pygame
import numpy as np
import track_m
import car
import config
import render

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Self Car")
clock = pygame.time.Clock()
running = True

car_x, car_y = (200, 170)
car_dx, car_dy = (-1, -0.2)
cars = car.Cars(config.N, config.SX, config.SY, config.SDX, config.SDY, config.INIT_SPEED)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    render.drawTrack(screen)
    cars.update(screen)

    # render.drawDot(screen, (car_x, car_y), 8, (255, 255, 0))
    # d, px, py = track_m.caclDistance(car_x, car_y, car_dx, car_dy)
    # render.drawLine(screen, (car_x, car_y, px, py))
    # pygame.draw.circle(screen, (100, 255, 100), render.to_screen(px, py), 6)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
