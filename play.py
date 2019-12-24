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
#warden = BaseSprite(WARDEN_IMAGE)
macgyver = BaseSprite(MACGYVER_IMAGE)

while True:
    maze1.display_map(window)
    macgyver.display(window)
    pygame.display.flip()
