import torch
import pygame
import config
import os
import json


def save_model(state_dict, score):
    if state_dict is None or score is None:
        return
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    data_path = os.path.join(config.MODEL_DIR, "data.json")

    try:
        with open(data_path, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    name = f"model{len(data) + 1}.pt"
    torch.save(state_dict, os.path.join(config.MODEL_DIR, name))
    data[name] = score

    with open(data_path, "w") as f:
        json.dump(data, f, indent=2)


def load_scores():
    try:
        with open(os.path.join(config.MODEL_DIR, "data.json"), "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def render_saved(screen):
    pygame.draw.rect(screen, (255, 255, 255), (config.SAVES_POS_X, config.SAVES_POS_Y, config.SAVES_W, config.SAVES_H), 2)
    pygame.draw.line(screen, (255, 255, 255), (config.SAVES_POS_X + 10, config.SAVES_POS_Y + 20), (config.SAVES_POS_X + config.SAVES_W - 10, config.SAVES_POS_Y + 20), 2)
    pygame.draw.line(screen, (255, 255, 255), (config.SAVES_POS_X + config.SAVES_W * 0.75, config.SAVES_POS_Y + 10), (config.SAVES_POS_X + config.SAVES_W * 0.75, config.SAVES_POS_Y + config.SAVES_H - 10), 2)

    font = pygame.font.Font(None, 16)
    text_m = font.render("Models", True, (255, 255, 255))
    text_sc = font.render("Scores", True, (255, 255, 255))
    screen.blit(text_m, (config.SAVES_POS_X + 10, config.SAVES_POS_Y + 8))
    screen.blit(text_sc, (config.SAVES_POS_X + config.SAVES_W * 0.75 + 4, config.SAVES_POS_Y + 8))
    text_i1 = font.render('Press "S" to save current', True, (255, 255, 255))
    screen.blit(text_i1, (config.SAVES_POS_X, config.SAVES_POS_Y + config.SAVES_H + 6))
    text_i2 = font.render('Arrow keys to select model, "L" to load', True, (255, 255, 255))
    screen.blit(text_i2, (config.SAVES_POS_X, config.SAVES_POS_Y + config.SAVES_H + 21))
    text_i3 = font.render('Press "P" to pause simulation', True, (255, 255, 255))
    screen.blit(text_i3, (config.SAVES_POS_X, config.SAVES_POS_Y + config.SAVES_H + 36))
    text_i4 = font.render('Press "R" to reset generation', True, (255, 255, 255))
    screen.blit(text_i4, (config.SAVES_POS_X, config.SAVES_POS_Y + config.SAVES_H + 51))

    data = load_scores()
    offset = 0
    for filename, score in sorted(data.items(), key=lambda x: x[1] if x[1] is not None else float("-inf"), reverse=True)[:15]:
        text_m = font.render(f"{filename}", True, (255, 255, 255))
        text_s = font.render(f"{score}", True, (255, 255, 255))
        screen.blit(text_m, (config.SAVES_POS_X + 10, config.SAVES_POS_Y + 26 + offset))
        screen.blit(text_s, (config.SAVES_POS_X + config.SAVES_W * 0.75 + 4, config.SAVES_POS_Y + 26 + offset))
        offset += 15