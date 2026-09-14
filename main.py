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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        print(1)
    if keys[pygame.K_RIGHT]:
        print(2)
    if keys[pygame.K_UP]:
        print(3)
    if keys[pygame.K_DOWN]:
        print(4)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
