#! /usr/bin/env python3
# coding: utf-8

import time
import pygame

#~ from classes import GameManager, Control, Warden, MacGyver, Tools

from display import Warden, MacGyver, Tools, Map
from manager import MapManager, GameManager, Control

from constants import (
    HOMEPAGE_IMAGE,
    TOOL_LIST,
    MACGYVER_IMAGE,
    WARDEN_IMAGE,
    SPRITE_SIZE,
    SPRITES_NUMBER,
    MAP1
)

game = GameManager(pygame)

maze = MapManager(pygame, MAP1)

# opening of window Pygame

window = maze.window()

# sounds objects:

win_sound = maze.win_sound()
game_over_sound = maze.game_over_sound()

# Initialize control object:

control = Control()

# Game loop:

while control.game:

    maze.display(HOMEPAGE_IMAGE, window)

    control.over = True
    control.win = True
    control.lose = False
    control.selected = False

    while control.home_page:
        game.handle_input_home(control, maze)

    maze.game_info(window, "Picked up tools:")
    guard = Warden(WARDEN_IMAGE)
    guard.position(14, 14)
    macgyver = MacGyver(maze, MACGYVER_IMAGE)
    macgyver.position()

    list_tool = []
    for tool_name, tool_image in TOOL_LIST.items():
        tool = Tools(maze, tool_image, tool_name)
        tool.position()
        tool.place_item(game)
        list_tool.append(tool)

    grabbed_tools = []

    while control.playing:
        game.handle_input(macgyver, time, control)

        maze.display_map(window)
        macgyver.check_tools(list_tool, grabbed_tools)
        if control.win is True:
            macgyver.display(window)
        if control.lose is False:
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

        game.check_victory_condition(
            macgyver, grabbed_tools, control, win_sound, game_over_sound, maze, window
        )

        pygame.display.flip()
