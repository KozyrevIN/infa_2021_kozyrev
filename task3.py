import pygame
from pygame.draw import *
import pygame.freetype
import numpy as np


# человек с начальной координатой левого нижнего угла (x, y) и высотой h (координаты нормальные, а не сверху вниз!)
def draw_GORSHOK_JIIIIV(x, y, h):
    # футболка
    circle(screen, orange, (round(x + 500 * h / 800), screen_height - y), round(250 * h / 800))
    # тело
    circle(screen, skin, (round(x + 500 * h / 800), round(screen_height - y - h * 375 / 800)), round(250 * h / 800))
    line(screen, skin, (round(x + 250 * h / 800), round(screen_height - y - h * 150 / 800)),
         (round(x + 100 * h / 800), round(screen_height - y - h * 700 / 800)), width=round(50 * h / 800))
    line(screen, skin, (round(x + 750 * h / 800), round(screen_height - y - h * 150 / 800)),
         (round(x + 900 * h / 800), round(screen_height - y - h * 700 / 800)), width=round(50 * h / 800))
    # рукава
    polygon(screen, orange,
            [(round(x + 290 * h / 800), round(screen_height - y - 90 * h / 800)),
             (round(x + 330 * h / 800), round(screen_height - y - 180 * h / 800)),
             (round(x + 270 * h / 800), round(screen_height - y - 240 * h / 800)),
             (round(x + 190 * h / 800), round(screen_height - y - 190 * h / 800)),
             (round(x + 200 * h / 800), round(screen_height - y - 100 * h / 800))])
    polygon(screen, black,
            [(round(x + 290 * h / 800), round(screen_height - y - 90 * h / 800)),
             (round(x + 330 * h / 800), round(screen_height - y - 180 * h / 800)),
             (round(x + 270 * h / 800), round(screen_height - y - 240 * h / 800)),
             (round(x + 190 * h / 800), round(screen_height - y - 190 * h / 800)),
             (round(x + 200 * h / 800), round(screen_height - y - 100 * h / 800))], width=1)
    polygon(screen, orange,
            [(round(x + 710 * h / 800), round(screen_height - y - 90 * h / 800)),
             (round(x + 670 * h / 800), round(screen_height - y - 180 * h / 800)),
             (round(x + 730 * h / 800), round(screen_height - y - 240 * h / 800)),
             (round(x + 810 * h / 800), round(screen_height - y - 190 * h / 800)),
             (round(x + 800 * h / 800), round(screen_height - y - 100 * h / 800))])
    polygon(screen, black,
            [(round(x + 710 * h / 800), round(screen_height - y - 90 * h / 800)),
             (round(x + 670 * h / 800), round(screen_height - y - 180 * h / 800)),
             (round(x + 730 * h / 800), round(screen_height - y - 240 * h / 800)),
             (round(x + 810 * h / 800), round(screen_height - y - 190 * h / 800)),
             (round(x + 800 * h / 800), round(screen_height - y - 100 * h / 800))], width=1)
    # ладони
    ellipse(screen, skin, (round(x + 70 * h / 800), round(screen_height - y - 790 * h / 800),
                           round(80 * h / 800), round(160 * h / 800)))
    ellipse(screen, white, (round(x + 70 * h / 800), round(screen_height - y - 790 * h / 800),
                            round(80 * h / 800), round(160 * h / 800)), width=1)
    ellipse(screen, skin, (round(x + 850 * h / 800), round(screen_height - y - 790 * h / 800),
                           round(80 * h / 800), round(160 * h / 800)))
    ellipse(screen, white, (round(x + 850 * h / 800), round(screen_height - y - 790 * h / 800),
                            round(80 * h / 800), round(160 * h / 800)), width=1)
    # рот
    polygon(screen, red, [(round(x + 500 * h / 800), round(screen_height - y - 220 * h / 800)),
                          (round(x + 350 * h / 800), round(screen_height - y - 300 * h / 800)),
                          (round(x + 650 * h / 800), round(screen_height - y - 300 * h / 800))])
    polygon(screen, black, [(round(x + 500 * h / 800), round(screen_height - y - 220 * h / 800)),
                            (round(x + 350 * h / 800), round(screen_height - y - 300 * h / 800)),
                            (round(x + 650 * h / 800), round(screen_height - y - 300 * h / 800))], width=1)
    # глаза
    ellipse(screen, blue, (round(x + 350 * h / 800), (screen_height - y - 480 * h / 800), 120 * h / 800, 100 * h / 800))
    ellipse(screen, black, (round(x + 350 * h / 800), (screen_height - y - 480 * h / 800), 120 * h / 800, 100 * h / 800)
            , width=1)
    ellipse(screen, blue, (round(x + 530 * h / 800), (screen_height - y - 480 * h / 800), 120 * h / 800, 100 * h / 800))
    ellipse(screen, black, (round(x + 530 * h / 800), (screen_height - y - 480 * h / 800), 120 * h / 800, 100 * h / 800)
            , width=1)
    ellipse(screen, black, (round(x + 395 * h / 800), (screen_height - y - 440 * h / 800), 30 * h / 800, 20 * h / 800))
    ellipse(screen, black, (round(x + 575 * h / 800), (screen_height - y - 440 * h / 800), 30 * h / 800, 20 * h / 800))
    # нос
    polygon(screen, brown, [(round(x + 500 * h / 800), round(screen_height - y - 330 * h / 800)),
                            (round(x + 530 * h / 800), round(screen_height - y - 360 * h / 800)),
                            (round(x + 470 * h / 800), round(screen_height - y - 360 * h / 800))])
    # волосы
    n = 12
    for k in range(3, n - 1):
        polygon(screen, purple,
                [((x + 500 * h / 800) + 330 * h / 800 * np.cos(np.pi / n * (k - 1 / 2)),
                  screen_height - y - h * 375 / 800 - 330 * h / 800 * np.sin(np.pi / n * (k - 1 / 2))),
                 ((x + 500 * h / 800) + 250 * h / 800 * np.cos(np.pi / n * (k - 1)),
                  screen_height - y - h * 375 / 800 - 250 * h / 800 * np.sin(np.pi / n * (k - 1))),
                 ((x + 500 * h / 800) + 250 * h / 800 * np.cos(np.pi / n * k),
                  screen_height - y - h * 375 / 800 - 250 * h / 800 * np.sin(np.pi / n * k))], 0)


# Рисование плаката с начальными координатами x0 b y0, размерами dx и dy
def draw_poster(x, y, dx, dy, text, centering):
    rect(screen, green, (x, 800 - y, dx, dy))
    printed_text = PunkFont.render(text, True, black)
    screen.blit(printed_text, (centering, 10))


pygame.init()
PunkFont = pygame.font.SysFont('Arial Bold', 137)

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (135, 206, 250)
orange = (255, 165, 0)
purple = (238, 130, 238)
brown = (210, 105, 30)
green = (124, 252, 0)
skin = (255, 219, 172)

FPS = 30
screen_height = 700
screen_width = 1500
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(white)

x0, y0 = 680, 0
draw_GORSHOK_JIIIIV(x0, y0, 650)
x0, y0 = 0, 0
blue = (175, 225, 175)
purple = (255, 234, 0)
orange = (79, 121, 66)
draw_GORSHOK_JIIIIV(x0, y0, 650)
x0, y0 = 0, 800
draw_poster(x0, y0, 1500, 100, 'PYTHON is REALLY AMAZING', 50)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()