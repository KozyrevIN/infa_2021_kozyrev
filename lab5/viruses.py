import pygame
from pygame.draw import *
from pygame.mixer import *
import random
from random import randint
import numpy as np

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
    Checks if figure got hit by mouse, if it does adds points, plays sound and displays combo
    :param mouse: pygame.event.MOUSEBUTTONDOWN
    """
    global points
    x, y = mouse.pos[0], mouse.pos[1]
    hit = 0
    gathered_points = 0
    for i in range(num_balls):
        if (x - balls[i][1])**2 + (y - balls[i][2])**2 <= balls[i][5]**2:
            sound_ball.play()
            hit += 1
            gathered_points += int(100 / balls[i][5])
            balls[i] = new_ball()
    i = 0
    while i < len(viruses):
        if (x - viruses[i][1])**2 + (y - viruses[i][2])**2 <= viruses[i][0]**2:
            sound_virus.play()
            hit += 1
            gathered_points += 100
            for figure in balls:
                figure[0] = COLORS[randint(0, 5)]
            viruses.pop(i)
            i -= 1
        i += 1
    if hit == 0:
        points -= 5
    elif hit == 1:
        points += gathered_points
    if hit > 1:
        points += gathered_points * hit
        text_to_display.append(['combo x' + str(hit) + '!', 320, 0, RED, 2*FPS])
        viruses.append(new_virus())


def move_figures():
    """
    Updates position of figures based on their velocities
    """
    for figure in balls:
        figure[1], figure[2] = figure[1] + figure[3], figure[2] + figure[4]
        if figure[1] - figure[5] < 0:
            figure[1], figure[3] = figure[5], - figure[3]
        elif figure[1] + figure[5] > 1500:
            figure[1], figure[3] = 1500 - figure[5], - figure[3]
        if figure[2] - figure[5] < 0:
            figure[2], figure[4] = figure[5], - figure[4]
        elif figure[2] + figure[5] > 800:
            figure[2], figure[4] = 800 - figure[5], - figure[4]
    for figure in viruses:
        figure[3], figure[4] = figure[3] + randint(-1, 1), figure[4] + randint(-1, 1)
        figure[1], figure[2] = figure[1] + figure[3], figure[2] + figure[4]
        if figure[1] - figure[0] < 0:
            figure[1], figure[3] = figure[0], - figure[3]
        elif figure[1] + figure[0] > 1500:
            figure[1], figure[3] = 1500 - figure[0], - figure[3]
        if figure[2] - figure[0] < 0:
            figure[2], figure[4] = figure[0], - figure[4]
        elif figure[2] + figure[0] > 800:
            figure[2], figure[4] = 800 - figure[0], - figure[4]


def new_ball():
    """
    Creates new ball at a random position
    """
    x, y, r = randint(100, 1500), randint(100, 800), randint(10, 100)
    vx, vy = randint(-2, 2), randint(-2, 2)
    color = COLORS[randint(0, 5)]
    return [color, x, y, vx, vy, r]


def new_virus():
    """
    Creates new virus at a random position
    :rtype: object
    """
    x, y, r = randint(100, 1500), randint(100, 800), randint(50, 200)
    vx, vy = randint(-2, 2), randint(-2, 2)
    virus_arr = [r, x, y, vx, vy]
    return virus_arr


def display_figures():
    """
    Displays figures from the array
    """
    for figure in balls:
        circle(screen, figure[0], (figure[1], figure[2]), figure[5])
    for figure in viruses:
        virus_cur = pygame.transform.scale(virus, (int(2 * figure[0]), int(2 * 24/25*figure[0])))
        screen.blit(virus_cur, (int(figure[1] - figure[0]/2), int(figure[2] - figure[0]/2)))


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
    Shows finishing screen of a game with score of a player and leaderboard
    """
    global change_leaderboard, PAUSED, leaderboard
    screen.blit(Font_big.render('Your points ' + str(points), True, WHITE), (50, 50))
    screen.blit(Font.render('leaderboard (score, name, amount of balls, time)', True, BLUE), (50, 250))
    if change_leaderboard:
        input_leaders = open("leaderboard.txt", "r")
        leaderboard = input_leaders.readlines()
        input_leaders.close()
        output_leaders = open("leaderboard.txt", "w")
        for i in range(len(leaderboard)):
            leaderboard[i] = leaderboard[i].split()
            leaderboard[i][0] = int(leaderboard[i][0])
        leaderboard.append([points, name, str(num_balls), str(play_time)])
        leaderboard.sort(reverse=True)
        for i in range(len(leaderboard)):
            text = ''
            for j in range(len(leaderboard[i])):
                text += str(leaderboard[i][j]) + ' '
            output_leaders.write(text + '\n')
        output_leaders.close()
        change_leaderboard = False
    else:
        for i in range(min(len(leaderboard), 18)):
            text = ''
            for j in range(len(leaderboard[i])):
                text += str(leaderboard[i][j]) + ' '
            screen.blit(Font.render(text, True, WHITE), (50 + 700 * (i // 9), 300 + 50 * (i % 9)))


# Getting nickname
name = input('Введите имя (не более 20 символов) ')
if len(name) > 20:
    name = name[:20]

# Initializing PyGame
pygame.init()

# Music settings
music.load('theme.wav')
music.play(loops=100)
sound_ball = Sound('ball.wav')
sound_virus = Sound('virus.wav')

# Display settings
FPS = 60
screen = pygame.display.set_mode((1500, 800))
pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Font and game time settings
Font = pygame.font.SysFont('Comic Sans', 60)
Font_big = pygame.font.SysFont('Comic Sans', 250)
play_time = 60
num_balls = 30

# Starter game values
virus = pygame.image.load('coronavirus.png')
points = 0
timer = play_time * FPS
balls = [new_ball() for i in range(num_balls)]
viruses = []
text_to_display = []
leaderboard = []

PAUSED = False
change_leaderboard = True

# Main cycle, is done every frame
while not finished:
    clock.tick(FPS)

    # Event detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not PAUSED:
            is_hit(event)

    # Refreshing game values
    if timer > 0:
        move_figures()
        display_figures()
        display_text()
        timer -= 1
    else:
        finish()
        PAUSED = True

    # Updating screen
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()