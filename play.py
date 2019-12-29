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
print(maze1)
guard = Warden(WARDEN_IMAGE)
guard.position(14, 14)
macgyver = MacGyver(maze1, MACGYVER_IMAGE)
macgyver.position()

list_tool = []
for tool_name, tool_image in TOOL_LIST.items():
    tool = Tools(maze1, tool_image, tool_name)
    tool.position()
    tool.place_item(maze1)
    list_tool.append(tool)
    # print(list_tool[0].x)       

grabbed_tools = []
    
playing = True

while playing:
    for event in pygame.event.get():

        # To accelerate repeating key strokes:
        if event.type == KEYDOWN:
            if event.key == K_a:
                pygame.key.set_repeat(10,100)

        # To slow down with one move each key stroke:
        if event.type == KEYDOWN:
            if event.key == K_s:
                pygame.key.set_repeat()

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
    macgyver.check_tools(list_tool, grabbed_tools)
    macgyver.display(window)
    guard.display(window)
    for tool in list_tool:
        if tool.name not in grabbed_tools:
            tool.display(window)
    pygame.display.flip()
