import pgzrun
import random
from pgzero.actor import Actor
import pygame

WIDTH = 600
HEIGHT = 800

class BigPlatform:
    def __init__(self):
        self.actor = Actor('big_platform.png', center=(WIDTH // 2, 0))
        self.last = pygame.time.get_ticks()
        self.cooldown = 10000

    def update(self, paddle):
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

class HeartBonusLife:
    def __init__(self, x, y, generate_time: int, hearts_alive):
        self.actor = Actor('heart.png', center=(x, y))
        self.last = pygame.time.get_ticks()
        self.cooldown = generate_time * 1000
        self.hide = True
        self.hearts_alive = hearts_alive

    def draw(self):
        self.actor.draw()

    def update(self, paddle, Heart):
        if not self.hide:
            self.actor.y += 5

        if self.actor.colliderect(paddle.actor):
            self.hearts_alive.append(Heart(len(self.hearts_alive)))
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