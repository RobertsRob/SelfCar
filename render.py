import pygame
import track_m
import config

def to_screen(x, y):
    x = float(x)
    y = float(y)
    return (config.WIDTH // 2 + x, config.HEIGHT // 2 - y)

def drawLine(screen, points, color=(255, 255, 255)):
    x1, y1, x2, y2 = points
    pygame.draw.line(screen, color, to_screen(x1, y1), to_screen(x2, y2), 2)

def drawDot(screen, pos, radius, color):
    x, y = pos
    pygame.draw.circle(screen, color, to_screen(x, y), radius)


def drawTrack(screen):
    for i in range(len(track_m.render_inner_x1)):
        drawLine(screen, (track_m.render_inner_x1[i], track_m.render_inner_y1[i], track_m.render_inner_x2[i], track_m.render_inner_y2[i]))

    for i in range(len(track_m.render_outer_x1)):
        drawLine(screen, (track_m.render_outer_x1[i], track_m.render_outer_y1[i], track_m.render_outer_x2[i], track_m.render_outer_y2[i]))

def drawCheckpoints(screen):
    for i in range(len(track_m.render_inner_x1)):
        drawLine(screen, (track_m.render_checkpoints_x1[i], track_m.render_checkpoints_y1[i], track_m.render_checkpoints_x2[i], track_m.render_checkpoints_y2[i]), (0, 100, 0))


def drawText(screen, text, px, py):
    font = pygame.font.Font(None, 36)
    text_r = font.render(text, True, (255, 255, 255))
    screen.blit(text_r, (px, py))


updateN = 0
ludt = 1
def displayFPS(screen, dt):
    global updateN
    global ludt
    updateN += 1
    font = pygame.font.Font(None, 36)
    text = font.render("fps: " + str(ludt), True, (255, 255, 255))
    screen.blit(text, (20, 20))
    if updateN % (config.MAX_FPS // 4) == 0:
        ludt = round(1 / dt, 1)


def drawPause(screen):
    SW = config.WIDTH
    SH = config.HEIGHT
    w, h = 400, 140
    pygame.draw.rect(screen, (0, 0, 0), (SW / 2 - w / 2, SH / 2 - h / 2, w, h))
    pygame.draw.rect(screen, (255, 255, 255), (SW / 2 - w / 2, SH / 2 - h / 2, w, h), 2)
    font = pygame.font.Font(None, 100)
    text = font.render("Paused", True, (255, 255, 255))
    screen.blit(text, (SW / 2 - w / 4 - 25, SH / 2 - h / 4))