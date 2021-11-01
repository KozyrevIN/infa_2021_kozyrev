import math
import random
from random import *
import pygame


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
HEIGHT = 600


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
            self.x, self.vx = self.r, - int(0.8 * self.vx)
        elif self.x > WIDTH - self.r:
            self.x, self.vx = WIDTH - self.r, - int(0.8 * self.vx)
        if self.y < self.r:
            self.y, self.vy = self.r, - int(0.8 * self.vy)
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
        self.x = 0
        self.y = 550

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
        screen.blit(syringe_cur, (int(self.x), int(self.y)))
        #pygame.draw.line(self.screen, self.color, (40, 450),
                         #(40 + self.f2_power * math.cos(self.an), 450 + self.f2_power * math.sin(self.an)), width=20)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


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


def display_point():
    screen.blit(Font.render('Your points: ' + str(points), True, BLACK), (25, 25))


pygame.init()
Font = pygame.font.SysFont('Comic Sans', 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
points = 0
balls = []

viruses = [pygame.image.load('files/pictures/virus_1.png'), pygame.image.load('files/pictures/virus_2.png')]
syringes = [pygame.image.load('files/pictures/syringe_normal.png'), pygame.image.load('files/pictures/syringe_red.png')]

clock = pygame.time.Clock()
gun = Gun(screen)
number_of_targets = 2
targets = [Target() for i in range(number_of_targets)]
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        t.draw()
    for b in balls:
        b.draw()
    display_point()
    pygame.display.update()

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

pygame.quit()
