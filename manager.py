"""Manage the control of the game"""

import pygame

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
    MAP1,
    MAP2,
    COLOR_WIN,
    COLOR_LOSE,
)

from display import Map


class Control:
    """Class to control the value of boolans needed for several methods"""

    def __init__(
            self,
            game=True,
            home_page=True,
            selected=False,
            playing=False,
            over=True,
            win=True,
            lose=False,
    ):
        self.game = game
        self.home_page = home_page
        self.selected = selected
        self.playing = playing
        self.over = over
        self.win = win
        self.lose = lose


class GameManager(Map):
    def __init__(self, pygame):
        self.pygame = pygame.init()
        super().__init__()

    def window(self):
        return pygame.display.set_mode((WINDOW_WIDE, WINDOW_LENGTH))

    def win_sound(self):
        return pygame.mixer.Sound(WIN_SOUND)

    def game_over_sound(self):
        return pygame.mixer.Sound(GAME_OVER_SOUND)

    def home_page(self, homepage, window):
        self.homepage = homepage
        page = pygame.image.load(self.homepage).convert()
        window.blit(page, (0, 0))

    def display(self, HOMEPAGE_IMAGE, window):
        self.home_page(HOMEPAGE_IMAGE, window)
        pygame.display.flip()

    def get_input(self):
        return pygame.event.get()

    def handle_input_home(self, control):
        for event in self.get_input():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                control.game = False
                control.home_page = False
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    if control.selected is True:
                        control.home_page = False
                        control.playing = True
                if event.key == K_F1:
                    control.selected = True
                    maze = Map(MAP1)
                elif event.key == K_F2:
                    control.selected = True
                    maze = Map(MAP2)

    def handle_input(self, macgyver, time, control):
        for event in self.get_input():

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

    def check_victory_condition(
            self, macgyver, grabbed_tools, control, win_sound, game_over_sound, maze, window
    ):
        if (
                macgyver.case_num_x == 14
                and macgyver.case_num_y == 14
                and len(grabbed_tools) == 3
        ):
            if control.over is True:
                print("You win!")
                """SOUND settings"""
                win_sound.play()
            control.over = False
            control.lose = True
            maze.warden_asleep_info(
                window, "You win! You put to sleep the guard!", COLOR_WIN
            )
        elif (
                macgyver.case_num_x == 14
                and macgyver.case_num_y == 14
                and len(grabbed_tools) != 3
        ):
            maze.warden_asleep_info(window, "You lose! GAME OVER", COLOR_LOSE)
            if control.over is True:
                print("You lose!")
                """SOUND settings"""
                game_over_sound.play()
            control.win = False
            control.over = False
