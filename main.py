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
    dt = clock.tick(config.MAX_FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    render.drawTrack(screen)
    cars.update(screen, dt)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        print("UP")
    if keys[pygame.K_DOWN]:
        print("DOWN")
    if keys[pygame.K_RIGHT]:
        cars.steerAll(-config.ROT_SPEED, dt)
    if keys[pygame.K_LEFT]:
        cars.steerAll(config.ROT_SPEED, dt)

    render.displayFPS(screen, dt)

    pygame.display.update()

pygame.quit()
