#! /usr/bin/env python3
# coding: utf-8

import pygame
import time

from pygame.locals import *

from classes import *
from constants import *

pygame.init()

#opening of window Pygame

# window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
window = pygame.display.set_mode((WINDOW_WIDE, WINDOW_LENGTH))

maze1 = Map(MAP2)
maze1.game_info(window, "Picked up tools:")
guard = Warden(WARDEN_IMAGE)
guard.position(14, 14)
macgyver = MacGyver(maze1, MACGYVER_IMAGE)
macgyver.position()

#sounds objects:

win_sound = pygame.mixer.Sound(WIN_SOUND)
game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

list_tool = []
for tool_name, tool_image in TOOL_LIST.items():
    tool = Tools(maze1, tool_image, tool_name)
    tool.position()
    tool.place_item(maze1)
    list_tool.append(tool)

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

    """Display tools if they haven't been taken"""
    
    for tool in list_tool:
        if tool.name not in grabbed_tools:
            tool.display(window)

    """Display picked tools"""
    for idx, tools in enumerate(grabbed_tools):
        for tool in list_tool:
            if tools == tool.name:
                tool.x = (idx + 6) * SPRITE_SIZE
                tool.y = SPRITES_NUMBER * SPRITE_SIZE
                tool.display(window)
        
    """Check items' number when MacGyver reach the warden:"""
    
    if macgyver.case_number_x == 14 and macgyver.case_number_y == 14 and len(grabbed_tools) == 3:
        win_sound.play()
        print("You win!")
        maze1.warden_asleep_info(window, "You win! You asleepped the warden!", COLOR_WIN)
        time.sleep(3)
        playing = False
    elif macgyver.case_number_x == 14 and macgyver.case_number_y == 14 and len(grabbed_tools) != 3:
        maze1.warden_asleep_info(window, "You lose! GAME OVER", COLOR_LOSE)
        game_over_sound.play()
        print("You lose!")
        time.sleep(3)
        playing = False

    pygame.display.flip()

