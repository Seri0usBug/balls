import pygame
from pygame.draw import *
from random import randint
import settings as st

Time = 0

class Ball:
    def __init__(self, x, y, min_r=10, max_r=100):
        self.color = st.COLORS[randint(0, len(st.COLORS) - 1)]
        self.radius = randint(min_r, max_r)
        self.initial_radius = self.radius
        self.x = x
        self.y = y
        self.v = 0
        self.time_create = Time
        self.time_live = st.FPS * 15 + randint(-5*st.FPS, 10*st.FPS)

    def update(self, is_updated):
        if is_updated:
            self.v += st.G * st.dT / 2
            self.y += self.v * st.dT
        self.radius = int((1 - (Time - self.time_create) / self.time_live) * self.initial_radius)

    def reflect(self):
        self.y += self.v * st.dT
        self.v = -self.v

    def get_vyr(self):
        vyr = (self.v, self.y, self.radius)
        return vyr

    def draw(self, screen):
        if self.time_create + self.time_live > Time:
            circle(screen, self.color, (self.x, self.y), self.radius)
            circle(screen, st.BORDER_COLOR, (self.x, self.y), self.radius, int(0.05 * self.radius))

    def is_die(self):
        return (self.time_create + self.time_live) < Time

class Screen:
    def __init__(self, width, height, fps=30):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.balls = []
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def add_ball(self, ball):
        self.balls.append(ball)
        if len(self.balls) > st.CNT_BALLS:
            self.balls.pop(0)

    def update_and_draw(self):
        self.screen.fill(st.BG_COLOR)
        del_balls = []
        for i in range(len(self.balls)):
            v, y, r = self.balls[i].get_vyr()
            is_updated = not (abs(v) <= 2 and abs((y + r - self.height)) < 5)
            self.balls[i].update(is_updated)

            if y + r >= self.height and v > 0:
                self.balls[i].reflect()
            self.balls[i].draw(self.screen)

            if self.balls[i].is_die():
                del_balls.append(i)

        for i in reversed(range(len(del_balls))):
            self.balls.pop(del_balls[i])

        pygame.display.update()
        self.clock.tick(self.fps)
        global Time
        Time += 1

    def cnt_balls(self):
        return len(self.balls)

