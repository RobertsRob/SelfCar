import render
import pygame
import config

scores = [0.0]
best_score = 0
segments = []

def graph_draw(screen):
    # pygame.draw.rect(screen, (0, 0, 0), (config.GRAPH_POS_X, config.GRAPH_POS_Y, config.GRAPH_W, config.GRAPH_H))
    pygame.draw.rect(screen, (255, 255, 255), (config.GRAPH_POS_X, config.GRAPH_POS_Y, config.GRAPH_W, config.GRAPH_H), 2)

    pygame.draw.line(screen, (255, 255, 255), (config.GRAPH_POS_X + 35, config.GRAPH_POS_Y + 8), (config.GRAPH_POS_X + 35, config.GRAPH_POS_Y + config.GRAPH_H - 20), 2)
    pygame.draw.polygon(screen, (255, 255, 255), [(config.GRAPH_POS_X + 36, config.GRAPH_POS_Y + 8), (config.GRAPH_POS_X + 41, config.GRAPH_POS_Y + 16), (config.GRAPH_POS_X + 30, config.GRAPH_POS_Y + 16), (config.GRAPH_POS_X + 35, config.GRAPH_POS_Y + 8)])
    font = pygame.font.Font(None, 12)
    text_r = font.render(str(round(scores[-1], 1)), True, (255, 255, 255))
    text_r_0 = font.render(str(0), True, (255, 255, 255))
    screen.blit(text_r, (config.GRAPH_POS_X + 12, config.GRAPH_POS_Y + 20))
    screen.blit(text_r_0, (config.GRAPH_POS_X + 24, config.GRAPH_POS_Y + config.GRAPH_H - 20))
    pygame.draw.line(screen, (255, 255, 255), (config.GRAPH_POS_X + 35, config.GRAPH_POS_Y + config.GRAPH_H - 20), (config.GRAPH_POS_X + config.GRAPH_W - 16, config.GRAPH_POS_Y + config.GRAPH_H - 20), 2)
    pygame.draw.polygon(screen, (255, 255, 255), [(config.GRAPH_POS_X + config.GRAPH_W - 16, config.GRAPH_POS_Y + config.GRAPH_H - 20), (config.GRAPH_POS_X + config.GRAPH_W - 23, config.GRAPH_POS_Y + config.GRAPH_H - 25), (config.GRAPH_POS_X + config.GRAPH_W - 23, config.GRAPH_POS_Y + config.GRAPH_H - 14), (config.GRAPH_POS_X + config.GRAPH_W - 16, config.GRAPH_POS_Y + config.GRAPH_H - 20)])

    display_graph(screen)

def display_graph(screen):
    for segment in segments:
        pygame.draw.line(screen, (255, 255, 255), (segment[0], segment[1]), (segment[2], segment[3]), 2)

def calculate_segments():
    global scores, best_score, segments

    segments = []

    if best_score == 0 or len(scores) < 2:
        return
    av_h = config.GRAPH_POS_Y + config.GRAPH_H - 20 - (config.GRAPH_POS_Y + 8) - 6
    av_w = config.GRAPH_POS_X + config.GRAPH_W - 16 - (config.GRAPH_POS_X + 35)
    lpp = ()
    for i in range(len(scores)):
        p_y = av_h - scores[i] / best_score * av_h
        p_x = (i + 1) / len(scores) * av_w + 4
        tpp = (config.GRAPH_POS_X + 35 + p_x, config.GRAPH_POS_Y + 14 + p_y)
        if i != 0:
            segments.append((lpp[0], lpp[1], tpp[0], tpp[1]))
        lpp = tpp
        

def graph_data_update(this_gen_best_score):
    global best_score

    if scores[0] == 0.0:
        scores.pop(0)

    scores.append(this_gen_best_score)
    if this_gen_best_score > best_score:
        best_score = this_gen_best_score

    calculate_segments()