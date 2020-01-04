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

#sounds objects:

win_sound = pygame.mixer.Sound(WIN_SOUND)
game_over_sound = pygame.mixer.Sound(GAME_OVER_SOUND)

home = Homepage(HOMEPAGE_IMAGE)

playing = False
game = True
home_page = True

while game:

    home.show(window)
    pygame.display.flip()

    maze1 = Map(MAP1)
    maze1.game_info(window, "Picked up tools:")
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

    grabbed_tools = []

    over = True
    win = True
    lose = False

    while home_page:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                game = False
                home_page = False
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    playing = True
                    home_page = False
        
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
                time.sleep(1)
                playing = False
                home_page = True
                
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
        if win == True:
            macgyver.display(window)
        if lose == False:
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
            # win_sound.play()
            if over == True:
                print("You win!")
            over = False
            lose = True
            maze1.warden_asleep_info(window, "You win! You asleepped the warden!", COLOR_WIN)
        elif macgyver.case_number_x == 14 and macgyver.case_number_y == 14 and len(grabbed_tools) != 3:
            maze1.warden_asleep_info(window, "You lose! GAME OVER", COLOR_LOSE)
            # game_over_sound.play()
            if over == True:
                print("You lose!")
            win = False
            over = False

        pygame.display.flip()

