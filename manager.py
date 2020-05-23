"""Manage the control of the game"""

import pygame
import time

#~ from transitions import Machine

from pygame.locals import (
    K_F2,
    K_F1,
    K_KP_ENTER,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_RETURN,
    K_a,
    K_s,
    K_DOWN,
    K_UP,
    K_LEFT,
    K_RIGHT,
)

from constants import (
    WINDOW_WIDE,
    WINDOW_LENGTH,
    WIN_SOUND,
    GAME_OVER_SOUND,
    HOMEPAGE_IMAGE,
    MACGYVER_IMAGE,
    WARDEN_IMAGE,
    MAP1,
    MAP2,
    COLOR_WIN,
    COLOR_LOSE,
    TOOL_LIST,
    SPRITE_SIZE,
    SPRITES_NUMBER,
)

from display import Map, MacGyver, Warden, Tools, Home


class Control:
    """Class to control the value of boolans needed for several methods"""

    def __init__(
            self,
            over=True,
            win=True,
            lose=False,
            maze_choice=None,
    ):
        self.over = over
        self.win = win
        self.lose = lose
        self.maze_choice = maze_choice

control=Control()

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.maze = Map(pygame, MAP1)

class Menu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        self.home = Home(pygame)
        self.wind=self.home.window()

    def get_event(self, event):

        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            self.done = False
            self.quit = True

        if event.type == KEYDOWN:
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                if control.maze_choice is not None:
                    self.done = True
            if event.key == K_F1:
                control.maze_choice = MAP1
            elif event.key == K_F2:
                control.maze_choice = MAP2

    def update(self, HOMEPAGE_IMAGE):
        self.home.display(HOMEPAGE_IMAGE, self.wind)

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'

        control.over = True
        control.win = True
        control.lose = False

        if control.maze_choice == MAP1 or control.maze_choice == None:
            self.maze.__init__(pygame, MAP1)
            control.maze_choice = None
        elif control.maze_choice == MAP2:
            self.maze.__init__(pygame, MAP2)
            control.maze_choice = None

        self.window = self.maze.window()
        self.maze.game_info(self.window, "Picked up tools:")
        self.win_sound = self.maze.win_sound()
        self.game_over_sound = self.maze.game_over_sound()
        self.guard = Warden(WARDEN_IMAGE)
        self.guard.position(14, 14)
        self.macgyver = MacGyver(self.maze, MACGYVER_IMAGE)
        self.macgyver.position()

        self.list_tool = []
        for tool_name, tool_image in TOOL_LIST.items():
            tool = Tools(self.maze, tool_image, tool_name)
            tool.position()
            tool.place_item(self.maze)
            self.list_tool.append(tool)

        self.grabbed_tools = []

    def get_event(self, event):
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
            self.done = True

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.macgyver.move("right")
            if event.key == K_LEFT:
                self.macgyver.move("left")
            if event.key == K_UP:
                self.macgyver.move("up")
            if event.key == K_DOWN:
                self.macgyver.move("down")

    def update(self):

        self.maze.display_map(self.window)
        self.macgyver.check_tools(self.list_tool, self.grabbed_tools)

        if control.win is True:
            self.macgyver.display(self.window)
        if control.lose is False:
            self.guard.display(self.window)

        """Display tools if they haven't been taken"""

        for tool in self.list_tool:
            if tool.name not in self.grabbed_tools:
                tool.display(self.window)

        """Display picked tools"""
        for idx, tools in enumerate(self.grabbed_tools):
            for tool in self.list_tool:
                if tools == tool.name:
                    tool.x = (idx + 6) * SPRITE_SIZE
                    tool.y = SPRITES_NUMBER * SPRITE_SIZE
                    tool.display(self.window)

        """Check items' number when MacGyver reach the warden:"""

        if (
            self.macgyver.case_num_x == 14
            and self.macgyver.case_num_y == 14
            and len(self.grabbed_tools) == 3
        ):
            if control.over is True:
                print("You win!")
                """SOUND settings"""
                self.win_sound.play()
                control.over = False
                control.lose = True
                self.maze.warden_asleep_info(
                    self.window, "You win! You put to sleep the guard!", COLOR_WIN
                )
        elif (
                self.macgyver.case_num_x == 14
                and self.macgyver.case_num_y == 14
                and len(self.grabbed_tools) != 3
        ):
            self.maze.warden_asleep_info(self.window, "You lose! GAME OVER", COLOR_LOSE)
            if control.over is True:
                print("You lose!")
                """SOUND settings"""
                self.game_over_sound.play()
            control.win = False
            control.over = False

        pygame.display.flip()
 
class Manage:
    def __init__(self):
        self.done = False
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        if self.state_name == "game":
            self.state.__init__()
    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        if self.state_name=="menu":
            self.state.update(HOMEPAGE_IMAGE)
        elif self.state_name=="game":
            self.state.update()
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            pygame.display.update()
