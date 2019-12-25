#! /usr/bin/env python3
# coding: utf-8

import pygame
from pygame.locals import *

from classes import *
from constants import *

pygame.init()

#opening of window Pygame

window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

maze1 = Map(MAP1)
guard = Warden(WARDEN_IMAGE)
macgyver = MacGyver(maze1, MACGYVER_IMAGE)

playing = True

while playing:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            playing = False
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                macgyver.move('right')
            if event.key == K_LEFT:
                macgyver.move('left')
            if event.key == K_UP:
                macgyver.move('up')
            if event.key == K_DOWN:
                macgyver.move('down')
            
    maze1.display_map(window)
    macgyver.display(window)
    guard.display(window)
    pygame.display.flip()
