import pygame
from pygame.draw import *


def drawman(x):
    # футболка
    circle(screen, orange, (x + 500, 800), 250)
    # тело
    circle(screen, skin, (x + 500, 425), 250)
    line(screen, skin, (x + 250, 650), (x + 100, 100), width=50)
    line(screen, skin, (x + 750, 650), (x + 900, 100), width=50)
    # рукава


pygame.init()

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
screen = pygame.display.set_mode((1000, 800))
screen.fill(white)

x0 = 0
# человек с начальной координатой левого нижнего угла (x0, 0)
drawman(x0)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()