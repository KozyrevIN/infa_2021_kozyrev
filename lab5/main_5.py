import pygame
from pygame.draw import *
from random import randint
pygame.init()

# Display settings
FPS = 60
screen = pygame.display.set_mode((1500, 800))

# Colours
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
WHITE = (255, 255, 255)


def is_hit(mouse):
    """
    Checks if figure got hit by mouse, if it is adds points and displays combo
    :param mouse: pygame.event.MOUSEBUTTONDOWN
    """
    global points
    x, y = mouse.pos[0], mouse.pos[1]
    hit = 0
    gathered_points = 0
    for i in range(num_figures):
        if (x - figures[i][1])**2 + (y - figures[i][2])**2 <= figures[i][5]**2:
            hit += 1
            gathered_points += int(100 / figures[i][5])
            figures[i] = new_figure()
    if hit == 0:
        points -= 5
    elif hit == 1:
        points += gathered_points
    if hit > 1:
        points += gathered_points * hit
        text_to_display.append(['combo x' + str(hit) + '!', 320, 0, RED, 2*FPS])


def move_figures():
    """
    Updates position of figures based on their velocities
    """
    for figure in figures:
        figure[1], figure[2] = figure[1] + figure[3], figure[2] + figure[4]
        if figure[1] - figure[5] < 0:
            figure[1], figure[3] = figure[5], - figure[3]
        elif figure[1] + figure[5] > 1500:
            figure[1], figure[3] = 1500 - figure[5], - figure[3]
        if figure[2] - figure[5] < 0:
            figure[2], figure[4] = figure[5], - figure[4]
        elif figure[2] + figure[5] > 800:
            figure[2], figure[4] = 800 - figure[5], - figure[4]


def new_figure():
    """
    Creates new figure at a random position
    """
    x = randint(100, 1500)
    y = randint(100, 800)
    r = randint(10, 100)
    vx = randint(-2, 2)
    vy = randint(-2, 2)
    color = COLORS[randint(0, 5)]
    return [color, x, y, vx, vy, r]


def display_figures():
    """
    Displays figures from the array
    """
    for figure in figures:
        circle(screen, figure[0], (figure[1], figure[2]), figure[5])


def display_text():
    """
    Displays time, points and combo information
    """
    screen.blit(Font.render('points: ' + str(points), True, WHITE), (20, 0))
    screen.blit(Font.render('time left: ' + str(timer // FPS) + 's', True, WHITE), (20, 50))
    for i in range(len(text_to_display)):
        text = Font.render(text_to_display[i][0], True, text_to_display[i][3])
        screen.blit(text, (text_to_display[i][1], text_to_display[i][2] + i * 50))
        text_to_display[i][4] -= 1
    i = 0
    while i < len(text_to_display):
        if text_to_display[i][4] <= 0:
            text_to_display.pop(i)
        else:
            i += 1


def finish():
    """
    Shows finishing screen of a game
    """
    screen.blit(Font_big.render('Ваши очки: ' + str(points), True, WHITE), (50, 300))

# Setting display
pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Font and game time settings
Font = pygame.font.SysFont('Comic Sans', 60)
Font_big = pygame.font.SysFont('Comic Sans', 250)
play_time = 60
num_figures = 30

# Setting starter game values
points = 0
timer = play_time * FPS
figures = [new_figure() for i in range(num_figures)]
text_to_display = []

# Main cycle, is done every frame
while not finished:
    clock.tick(FPS)

    # Event detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_hit(event)

    # Refreshing game values
    if timer > 0:
        move_figures()
        display_figures()
        display_text()
        timer -= 1
    else:
        finish()

    # Updating screen
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
