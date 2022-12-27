import pgzrun
import random
from pgzero.actor import Actor
import pyautogui

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

    def draw(self):
        self.actor.draw()


class Heart:
    def __init__(self,x):
        self.actor = Actor('heart.png', center=(20+26*x,22))

    def draw(self):
        self.actor.draw()


paddle = Paddle()
hearts_alive = []
for i in range(3):
    hearts_alive.append(Heart(i))
ball = Ball(5)

def draw():
    screen.clear()
    paddle.draw()
    ball.draw()
    for heart in hearts_alive:
        heart.draw()


def update(dt):
    ball.update()
    paddle.update(ball)


def on_mouse_move(pos):
    x, y = pos
    paddle.actor.x = x


pgzrun.go()
