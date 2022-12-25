import pgzrun

WIDTH = 600
HEIGHT = 800


class Paddle:

    def __init__(self):
        self.actor = Actor('paddle.png', center=(WIDTH // 2, HEIGHT - 50))

    def draw(self):
        self.actor.draw()


paddle = Paddle()


def draw():
    screen.clear()
    paddle.draw()


def update(dt):
    pass


def on_mouse_move(pos):
    x, y = pos
    paddle.actor.x = x


pgzrun.go()
