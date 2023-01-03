import pgzrun
import random
from pgzero.actor import Actor
import pyautogui
import math
import pygame

WIDTH = 600
HEIGHT = 800


class Paddle:

    def __init__(self):
        self.actor = Actor('paddle.png', center=(WIDTH // 2, HEIGHT - 50))

    def update(self, ball):
        if self.actor.colliderect(ball.actor):
            ball.ball_dy *= -1
            ball.ball_dx *= 1 if random.randint(0, 1) else -1

    def draw(self):
        self.actor.draw()


class Ball:
    def __init__(self, speed: int):
        self.actor = Actor('ball.png', center=(WIDTH // 2, HEIGHT//2))
        self.speed = speed
        self.ball_dx = self.speed
        self.ball_dy = self.speed
        self.radius = 11

    def update(self):
        self.actor.x += self.ball_dx
        self.actor.y += self.ball_dy

        if not (0 <= ball.actor.x <= WIDTH):
            self.ball_dx *= -1

        if not (0 <= ball.actor.y <= HEIGHT):
            self.ball_dy *= -1

        if ball.actor.y == HEIGHT:
            global hearts_alive
            hearts_alive.pop(len(hearts_alive)-1)
            if len(hearts_alive) == 0:
                pyautogui.alert("YOU'VE LOST")
                exit()
            self.actor.y = HEIGHT // 2
            self.actor.x = WIDTH // 2

    def hits(self):
        ball.ball_dy *= -1
        ball.ball_dx *= 1 if random.randint(0, 1) else -1

    def draw(self):
        self.actor.draw()


class Heart:
    def __init__(self,x):
        self.actor = Actor('heart.png', center=(20+26*x,22))

    def draw(self):
        self.actor.draw()


class HeartBonusLife:
    def __init__(self, x, y, generate_time: int):
        self.actor = Actor('heart.png', center=(x, y))
        self.last = pygame.time.get_ticks()
        self.cooldown = generate_time * 1000

    def draw(self):
        self.actor.draw()

    def update(self):
        pass


class Obstacle:
    def __init__(self, x, y, radius=11, color='red'):
        self.pos = (x, y)
        self.radius = radius
        self.color = color
        self.status = True

    def draw(self):
        if self.status:
            screen.draw.filled_circle(self.pos, self.radius, self.color)
        else:
            pass

    def hits(self, ball: Ball):
        distance = math.sqrt((ball.actor.x - self.pos[0])**2 +(ball.actor.y - self.pos[1])**2)
        return distance < 20


def create_barriers(n, dy, colors):

    barriers = []
    dx = WIDTH // (n + 1)
    for i in range(n):
        barriers.append(
            Obstacle(dx * (i + 1), dy, color=random.choice(colors))
        )

    for i in range(n - 1):
        curr = barriers[i]
        next = barriers[i + 1]
        barriers.append(
            Obstacle(curr.pos[0] + (next.pos[0] - curr.pos[0]) // 2, dy + 30, color=random.choice(colors))
        )
    return barriers


class BigPlatform:
    def __init__(self):
        self.actor = Actor('big_platform.png', center=(WIDTH // 2, 0))
        self.last = pygame.time.get_ticks()
        self.cooldown = 10000

    def update(self):
        self.actor.x += 1 if random.randint(0, 1) else 0
        self.actor.y += 5

        if self.actor.colliderect(paddle.actor):
            self.actor.x = 500
            self.actor.y = HEIGHT + 50
            paddle.actor = Actor('big_paddle.png',center=(paddle.actor.x, paddle.actor.y))
            self.last = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            paddle.actor = Actor('paddle.png',center=(paddle.actor.x, paddle.actor.y))

        if self.actor.y > HEIGHT + 50 and random.randint(0,10000) < 5:
            self.actor.x = WIDTH // 2
            self.actor.y = 0

    def draw(self):
        self.actor.draw()


paddle = Paddle()
hearts_alive = []
for i in range(3):
    hearts_alive.append(Heart(i))
ball = Ball(5)
platform = BigPlatform()
heart_bonus = HeartBonusLife(random.randint(10, WIDTH-10), -10, 30)

colors = ['red', 'green', 'yellow', 'blue']
barriers = create_barriers(10, 70, colors)


def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    platform.draw()
    heart_bonus.draw()
    for heart in hearts_alive:
        heart.draw()
    for item in barriers:
        item.draw()


def update(dt):
    ball.update()
    paddle.update(ball)
    platform.update()
    heart_bonus.update()
    for barrier in barriers:
        if barrier.hits(ball):
            barriers.remove(barrier)
            ball.hits()
    if len(barriers) == 0:
        pyautogui.alert("YOU'VE WON!")
        exit()


def on_mouse_move(pos):
    x, y = pos
    paddle.actor.x = x


pgzrun.go()
