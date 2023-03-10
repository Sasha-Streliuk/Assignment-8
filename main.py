import pgzrun
import random
from pgzero.actor import Actor
import pygame

WIDTH = 600
HEIGHT = 800
COLORS = {'red': 1, 'green': 2, 'yellow': 3, 'blue': 4}


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
            global loss
            hearts_alive.pop(len(hearts_alive)-1)
            if len(hearts_alive) == 0:
                loss = True
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
        self.hide = True

    def draw(self):
        self.actor.draw()

    def update(self):
        global hearts_alive
        if not self.hide:
            self.actor.y += 5

        if self.actor.colliderect(paddle.actor):
            hearts_alive.append(Heart(len(hearts_alive)))
            self.actor.pos = (-10, -10)
            self.hide = True

        if self.actor.y > HEIGHT + 20:
            self.actor.pos = (-10, -10)
            self.hide = True

        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            self.hide = False
            self.actor.pos = (random.randint(10, WIDTH - 10), 0)


class Obstacle:
    def __init__(self, x, y, width=40, height=20, color='red', strength=1):
        self.pos = (x, y)
        self.color = color
        self.width = width
        self.height = height
        self.strength = strength

    def draw(self):
        screen.draw.filled_rect(Rect(self.pos, (self.width, self.height)), self.color)

    def hits(self, ball: Ball):
        if (abs(self.pos[0] - ball.actor.x) <= 40) and (abs(self.pos[1] - ball.actor.y) <= 20):
            self.strength -= 1
            ball.ball_dy *= -1
            ball.ball_dx *= 1 if random.randint(0, 1) else -1
        return self.strength == 0


def create_barriers(n, dy, width, colors):

    barriers = []
    dx = (WIDTH - n * width) // (n + 1)
    for i in range(n):
        pos_x = dx * (i + 1) + width * i
        color = random.choice(colors)
        barriers.append(
            Obstacle(pos_x, dy, color=color, strength=COLORS[color])
        )

    for i in range(n - 1):
        curr = barriers[i]
        next = barriers[i + 1]
        pos_x = curr.pos[0] + (next.pos[0] - curr.pos[0]) // 2
        color = random.choice(colors)
        barriers.append(
            Obstacle(pos_x, dy + 30, color=color, strength=COLORS[color])
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


loss = False
paddle = Paddle()
hearts_alive = []
for i in range(3):
    hearts_alive.append(Heart(i))
ball = Ball(5)
platform = BigPlatform()
heart_bonus = HeartBonusLife(random.randint(10, WIDTH-10), -10, 30)
barriers = create_barriers(10, 70, 40, list(COLORS.keys()))


def draw():
    if loss:
        return
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
    if loss:
        screen.draw.text('Game Over', (170, 350), color="yellow", fontsize=75)
        return
    if len(barriers) == 0:
        screen.draw.text('   Win   ', (170, 350), color="yellow", fontsize=75)
        return
    ball.update()
    paddle.update(ball)
    platform.update()
    heart_bonus.update()
    for barrier in barriers:
        if barrier.hits(ball):
            barriers.remove(barrier)
            ball.hits()


def on_mouse_move(pos):
    x, y = pos
    paddle.actor.x = x


pgzrun.go()
