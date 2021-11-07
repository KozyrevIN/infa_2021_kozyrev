import math
from random import *
import pygame
from pygame.mixer import *


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 800


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 10 * FPS

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y += - self.vy
        self.vy -= 1
        if self.x < self.r:
            self.x, self.vx = self.r, - int(0.4 * self.vx)
        elif self.x > WIDTH - self.r:
            self.x, self.vx = WIDTH - self.r, - int(0.8 * self.vx)
        if self.y < self.r:
            self.y, self.vy = self.r, - int(0.4 * self.vy)
        elif self.y > HEIGHT - self.r:
            self.y, self.vy = HEIGHT - self.r, - int(0.8 * self.vy)

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        return (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2

    def timer(self):
        self.live -= 1
        return self.live


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.picture = syringes[0]
        self.x = 100
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        sound_syringe.play()

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        if self.f2_on:
            self.picture = syringes[1]
        else:
            self.picture = syringes[0]

    def draw(self):
        syringe_cur = pygame.transform.scale(self.picture, (int(40 + 2*self.f2_power), 100))
        syringe_cur = pygame.transform.rotate(syringe_cur, -360/6.18*self.an)
        x = self.x - abs(50 * math.sin(self.an))
        y = self.y - abs(50 * math.cos(self.an))
        if math.cos(self.an) < 0:
            x += (40 + 2 * self.f2_power) * math.cos(self.an)
        if math.sin(self.an) < 0:
            y += (40 + 2 * self.f2_power) * math.sin(self.an)
        screen.blit(syringe_cur, (x, y))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.picture = syringes[1]
        else:
            self.picture = syringes[0]

    def move(self, keys):
        if keys[pygame.K_w] and self.y > 100:
            gun.y -= 3
        elif keys[pygame.K_s] and self.y < HEIGHT - 100:
            gun.y += 3
        if keys[pygame.K_d] and self.x < WIDTH // 2 - 100:
            gun.x += 3
        elif keys[pygame.K_a] and self.x > 100:
            gun.x -= 3



class Target:

    def __init__(self):
        """ Инициализация новой цели. """
        self.live = True
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.vx = randint(-2, 2)
        self.vy = randint(-2, 2)
        self.r = randint(10, 50)
        self.color = RED
        self.screen = screen
        self.picture = choice(viruses)

    def move(self):
        if randint(0, 30) == 1:
            self.vx = randint(-2, 2)
            self.vy = randint(-2, 2)
        self.x += self.vx
        self.y += - self.vy
        if self.x < self.r:
            self.x, self.vx = self.r, - self.vx
        elif self.x > WIDTH - self.r:
            self.x, self.vx = WIDTH - self.r, - self.vx
        if self.y < self.r:
            self.y, self.vy = self.r, - self.vy
        elif self.y > HEIGHT - self.r:
            self.y, self.vy = HEIGHT - self.r, - self.vy

    def refresh_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.vx = randint(-2, 2)
        self.vy = randint(-2, 2)
        self.r = randint(10, 50)
        self.color = RED
        self.screen = screen
        self.picture = choice(viruses)

    def draw(self):
        virus_cur = pygame.transform.scale(self.picture, (int(2 * self.r), int(2 * self.r)))
        screen.blit(virus_cur, (int(self.x - self.r), int(self.y - self.r)))

    def hit(self):
        global points
        points += 1
        sound_virus.play()


def display_points():
    screen.blit(Font.render('SCORE ' + str(points), True, WHITE), (25, 25))


def finish():
    """
    Shows finishing screen of a game with score of a player and leaderboard
    """
    global change_leaderboard, leaderboard
    screen.fill(BLACK)
    screen.blit(Font_big.render('Вы уничтожили ' + str(points) + ' вирусов,', True, WHITE), (50, 50))
    screen.blit(Font_big.render('физтех выздоровел, но все равно', True, WHITE), (50, 100))
    screen.blit(Font_big.render('попал в дурку после сессии.', True, WHITE), (50, 150))
    screen.blit(Font.render('leaderboard (score, name, amount of viruses, time)', True, WHITE), (50, 250))
    input_leaders = open("leaderboard.txt", "r")
    leaderboard = input_leaders.readlines()
    input_leaders.close()
    output_leaders = open("leaderboard.txt", "w")
    for i in range(len(leaderboard)):
        leaderboard[i] = leaderboard[i].split()
        leaderboard[i][0] = int(leaderboard[i][0])
    leaderboard.append([points, name, number_of_targets, str(play_time)])
    leaderboard.sort(reverse=True)
    for i in range(len(leaderboard)):
        text = ''
        for j in range(len(leaderboard[i])):
            text += str(leaderboard[i][j]) + ' '
        output_leaders.write(text + '\n')
    output_leaders.close()
    for i in range(min(len(leaderboard), 18)):
        text = ''
        for j in range(len(leaderboard[i])):
            text += str(leaderboard[i][j]) + ' '
        screen.blit(Font.render(text, True, WHITE), (50 + 400 * (i // 9), 300 + 50 * (i % 9)))
    change_leaderboard = False
    pygame.display.update()



pygame.init()
Font = pygame.font.SysFont('Comic Sans', 40)
Font_big = pygame.font.SysFont('Comic Sans', 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
points = 0
play_time = 1
balls = []
leaderboard = []

viruses = [pygame.image.load('files/pictures/virus_1.png'), pygame.image.load('files/pictures/virus_2.png')]
syringes = [pygame.image.load('files/pictures/syringe_normal.png'), pygame.image.load('files/pictures/syringe_red.png')]
background = pygame.image.load('files/pictures/microscope.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
mask = pygame.image.load('files/pictures/microscope_mask.png')
mask = pygame.transform.scale(mask, (WIDTH, HEIGHT))

name = input('Введите имя (не более 10 символов) ')
if len(name) > 10:
    name = name[:10]

music.load('files/Sounds/theme.wav')
music.play(loops=-1)
sound_virus = Sound('files/Sounds/virus_explosion.wav')
sound_virus.set_volume(0.2)
sound_syringe = Sound('files/Sounds/syringe.wav')

clock = pygame.time.Clock()
gun = Gun(screen)
number_of_targets = 200
targets = [Target() for i in range(number_of_targets)]
finished = False

change_leaderboard = True
timer = FPS * play_time

while not finished:

    if timer > 0:
        screen.blit(Font_big.render('Вы уничтожили ' + str(points) + ' вирусов,', True, BLUE), (50, 50))

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            keys = pygame.key.get_pressed()
            gun.move(keys)

        screen.blit(background, (0, 0))
        gun.draw()
        for t in targets:
            t.draw()
        for b in balls:
            b.draw()
        screen.blit(mask, (0, 0))
        display_points()
        pygame.display.update()

        for t in targets:
            t.move()
        for b in balls:
            b.move()
            for t in targets:
                if b.hittest(t) and t.live:
                    t.live = False
                    t.hit()
                    t.refresh_target()
            if b.timer() <= 0:
                balls.remove(b)
        gun.power_up()
        timer -= 1
    elif change_leaderboard:

        finish()



screen.fill(BLACK)


pygame.quit()
