import pygame
import gameEntities as gaent
import settings as st
from random import randint


finished = False
my_screen = gaent.Screen(st.WIDTH, st.HEIGHT, st.FPS)

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    my_screen.update_and_draw()
    if my_screen.cnt_balls() < st.CNT_BALLS:
        x = randint(50, st.WIDTH - 50)
        y = randint(0, st.HEIGHT - 100)
        my_screen.add_ball(gaent.Ball(x, y))
