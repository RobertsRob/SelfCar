import pygame
import car
import config
import render
import torch
import copy
import time
import score_graph
import model_saves

pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Self Car")
clock = pygame.time.Clock()

pausedCar = False
running = True
best_model = None
best_score = None
generation = 1

cars = car.Cars(config.N, config.SX, config.SY, config.SDX, config.SDY, config.INIT_SPEED, best_model)
start_time = time.perf_counter()
time_from_start = 0.0

updates_from_start = 0

def resetGen():
    global cars, generation, best_model, best_score, updates_from_start, start_time, time_from_start
    best_index = torch.argmax(cars.points).item()
    best_model = copy.deepcopy(cars.models[best_index].state_dict())
    best_score = cars.points[best_index].item()

    print(f"Generation {generation} finished | " f"Best score: {best_score}")
    score_graph.graph_data_update(best_score)

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not pausedCar:
                resetGen()
            if event.key == pygame.K_p:
                pausedCar = not pausedCar
            if event.key == pygame.K_s:
                model_saves.save_model(best_model, best_score)

    screen.fill((0, 0, 0))

    render.drawTrack(screen)
    render.drawCheckpoints(screen)

    if not pausedCar:
        if cars.alive.any():
            cars.update(screen, dt, updates_from_start, time_from_start)
        else:
            resetGen()

    render.displayFPS(screen, dt)
    render.drawText(screen, "generation: " + str(generation), 20, 70)
    render.drawText(screen, "alive: " + str(cars.alive.sum().item()) + "/" + str(config.N), 20, 95)
    score_graph.graph_draw(screen)
    model_saves.render_saved(screen)

    if pausedCar:
        render.drawPause(screen)
    
    pygame.display.update()
   

pygame.quit()