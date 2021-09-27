import pygame
from pygame.draw import *

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill(white)

circle(screen, yellow, (200, 200), 150)
circle(screen, red, (130, 150), 40)
circle(screen, red, (270, 150), 30)
rect(screen, black, (125, 275, 150, 30))
circle(screen, black, (130, 150), 25)
circle(screen, black, (270, 150), 15)
polygon(screen, black, [(170, 140), (180, 120), (50, 50), (40, 70)])
polygon(screen, black, [(400-170, 140), (400-180, 120), (400-50, 50), (400-40, 70)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()