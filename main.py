import pygame
import car
import config
import render
import torch
import copy
import time

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Self Car")
clock = pygame.time.Clock()

running = True
best_model = None
generation = 1

cars = car.Cars(config.N, config.SX, config.SY, config.SDX, config.SDY, config.INIT_SPEED, best_model)
start_time = time.perf_counter()
time_from_start = 0.0

updates_from_start = 0

def resetGen():
    global cars, generation, best_model, updates_from_start, start_time, time_from_start
    best_index = torch.argmax(cars.points).item()
    best_model = copy.deepcopy(cars.models[best_index].state_dict())
    best_score = cars.points[best_index].item()
    print(f"Generation {generation} finished | " f"Best score: {best_score}")
    generation += 1
    cars = car.Cars(config.N, config.SX, config.SY, config.SDX, config.SDY, config.INIT_SPEED, best_model)
    updates_from_start = 0
    start_time = time.perf_counter()
    time_from_start = 0.0

while running:
    dt = clock.tick(config.MAX_FPS) / 1000.0

    time_from_start = time.perf_counter() - start_time
    updates_from_start += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    render.drawTrack(screen)
    render.drawCheckpoints(screen)

    if cars.alive.any():
        cars.update(screen, dt, updates_from_start, time_from_start)
    else:
        resetGen()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        resetGen()

    render.displayFPS(screen, dt)
    pygame.display.update()

pygame.quit()