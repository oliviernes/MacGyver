#! /usr/bin/env python3
# coding: utf-8

import pygame
import time

from pygame.locals import *

from classes import *
from constants import *

import pdb

#~ pygame.init()

game=Game_Manager(pygame)

# opening of window Pygame

window=game.window()

# sounds objects:

win_sound = game.win_sound()
game_over_sound = game.game_over_sound()

# Initialize control object:

control=Control()

# Initialize the maze:

maze=Map()

# Add functions used in the game loop:

def display():
    game.home_page(HOMEPAGE_IMAGE, window)
    pygame.display.flip()

def get_input():
    return pygame.event.get()

def handle_input_home():
    for event in get_input():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    control.game = False
                    control.home_page = False
                if event.type == KEYDOWN:
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        if control.selected == True:
                            control.home_page = False
                            control.playing = True
                    if event.key == K_F1:
                        control.selected = True
                        maze = Map(MAP1)
                    elif event.key == K_F2:
                        control.selected = True
                        maze = Map(MAP2)

def handle_input():
    for event in get_input():

        # To accelerate repeating key strokes:
        if event.type == KEYDOWN:
            if event.key == K_a:
                pygame.key.set_repeat(10, 100)

        # To slow down with one move each key stroke:
        if event.type == KEYDOWN:
            if event.key == K_s:
                pygame.key.set_repeat()

        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            time.sleep(1)
            control.playing = False
            control.home_page = True

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                macgyver.move("right")
            if event.key == K_LEFT:
                macgyver.move("left")
            if event.key == K_UP:
                macgyver.move("up")
            if event.key == K_DOWN:
                macgyver.move("down")

def check_victory_condition():
    if (
        macgyver.case_number_x == 14
        and macgyver.case_number_y == 14
        and len(grabbed_tools) == 3
    ):
        if control.over == True:
            print("You win!")
            """SOUND settings"""
            win_sound.play()
        control.over = False
        control.lose = True
        maze.warden_asleep_info(
            window, "You win! You asleepped the warden!", COLOR_WIN
        )
    elif (
        macgyver.case_number_x == 14
        and macgyver.case_number_y == 14
        and len(grabbed_tools) != 3
    ):
        maze.warden_asleep_info(window, "You lose! GAME OVER", COLOR_LOSE)
        if control.over == True:
            print("You lose!")
            """SOUND settings"""
            game_over_sound.play()
        control.win = False
        control.over = False

# Game loop:

while control.game:

    display()

    control.over = True
    control.win = True
    control.lose = False
    control.selected = False

    while control.home_page:
        handle_input_home()

    maze.game_info(window, "Picked up tools:")
    guard = Warden(WARDEN_IMAGE)
    guard.position(14, 14)
    macgyver = MacGyver(maze, MACGYVER_IMAGE)
    macgyver.position()

    list_tool = []
    for tool_name, tool_image in TOOL_LIST.items():
        tool = Tools(maze, tool_image, tool_name)
        tool.position()
        tool.place_item(maze)
        list_tool.append(tool)

    grabbed_tools = []

    while control.playing:
        handle_input()

        maze.display_map(window)
        macgyver.check_tools(list_tool, grabbed_tools)
        if control.win == True:
            macgyver.display(window)
        if control.lose == False:
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

        check_victory_condition()

        pygame.display.flip()
