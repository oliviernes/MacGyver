import pygame
from random import randint
from constants import (
    WINDOW_WIDE,
    WINDOW_LENGTH,
    WIN_SOUND,
    GAME_OVER_SOUND,
    WALL_IMAGE,
    FLOOR_IMAGE,
    SPRITES_NUMBER,
    SPRITE_SIZE,
    MAP1,
    TOOLS_SOUND,
)


class Map:
    """build the map from map*.txt files"""

    def __init__(self, pygame, map_file):
        self.pygame = pygame.init()
        """Generates an array in order to display the maze"""
        self.maze_array = self.parse_array(map_file)

    def parse_array(self, map_file):
        with open(map_file, "r") as maze_file:
            maze_list = []
            for line in maze_file:
                line_level = []
                for sprite in line:
                    if sprite != "\n":
                        line_level.append(sprite)
                maze_list.append(line_level)
        return maze_list

    def display_map(self, window):
        """display the map"""
        wall = pygame.image.load(WALL_IMAGE).convert()
        floor = pygame.image.load(FLOOR_IMAGE).convert()

        for idx_line, line in enumerate(self.maze_array):
            for idx_sprite, sprite in enumerate(line):
                x = idx_sprite * SPRITE_SIZE
                y = idx_line * SPRITE_SIZE
                if sprite == "m":
                    window.blit(wall, (x, y))
                elif sprite == "0" or "d" or "a":
                    window.blit(floor, (x, y))

    def game_info(self, window, msg):
        font = pygame.font.Font(None, 35)
        text1 = font.render(msg, True, (255, 255, 255), (36, 9, 239))
        window.blit(text1, (0, SPRITE_SIZE * SPRITES_NUMBER))

    def warden_asleep_info(self, window, msg, color_text):
        font = pygame.font.Font(None, 35)
        text2 = font.render(msg, True, color_text, (36, 9, 239))
        window.blit(text2, (0, SPRITE_SIZE * (SPRITES_NUMBER + 1)))
    
    def window(self):
        screen = pygame.display.set_mode((WINDOW_WIDE, WINDOW_LENGTH))
        color = [36, 9, 239]
        screen.fill(color)
        return screen

    def win_sound(self):
        return pygame.mixer.Sound(WIN_SOUND)

    def game_over_sound(self):
        return pygame.mixer.Sound(GAME_OVER_SOUND)


class BaseSprite:
    """Base class for objects"""

    def __init__(self, image):
        self.image = pygame.image.load(image).convert_alpha()

    def position(self, case_num_x=0, case_num_y=0):
        """return object's position"""
        self.case_num_x = case_num_x
        self.case_num_y = case_num_y
        self.x = self.case_num_x * SPRITE_SIZE
        self.y = self.case_num_y * SPRITE_SIZE
        return (self.x, self.y)

    def display(self, window):
        """Display the sprite on the window"""
        window.blit(self.image, (self.x, self.y))


class Warden(BaseSprite):
    """Class to display the warden"""

    def __init__(self, image):
        super().__init__(image)


class MacGyver(BaseSprite):
    """Class to display and move MacGyver"""

    def __init__(self, maze, image):
        self.maze = maze
        super().__init__(image)

    def move(self, direction):
        """move MacGiver according to the direction input"""
        if direction == "right":
            if self.case_num_x < (SPRITES_NUMBER - 1):
                if self.maze.maze_array[self.case_num_y][self.case_num_x + 1] != "m":
                    self.case_num_x += 1
                    self.x = self.case_num_x * SPRITE_SIZE

        if direction == "left":
            if self.case_num_x > 0:
                if self.maze.maze_array[self.case_num_y][self.case_num_x - 1] != "m":
                    self.case_num_x -= 1
                    self.x = self.case_num_x * SPRITE_SIZE

        if direction == "up":
            if self.case_num_y > 0:
                if self.maze.maze_array[self.case_num_y - 1][self.case_num_x] != "m":
                    self.case_num_y -= 1
                    self.y = self.case_num_y * SPRITE_SIZE

        if direction == "down":
            if self.case_num_y < (SPRITES_NUMBER - 1):
                if self.maze.maze_array[self.case_num_y + 1][self.case_num_x] != "m":
                    self.case_num_y += 1
                    self.y = self.case_num_y * SPRITE_SIZE

    def check_tools(self, list_tool, grabbed_tools):
        """Check grabbed tools and the inventory"""
        sound_tools = pygame.mixer.Sound(TOOLS_SOUND)
        for tool in list_tool:
            if self.x == tool.x and self.y == tool.y and tool.name not in grabbed_tools:
                grabbed_tools.append(tool.name)
                """SOUND settings"""
                sound_tools.play()
                print("You grabbed a " + tool.name + "!")
                print("Your tools:" + str(grabbed_tools))


class Tools(BaseSprite):
    """to instance and display MacGyver's objects"""

    def __init__(self, maze, image, name):
        super().__init__(image)
        self.maze = maze
        self.name = name

    def place_item(self, maze):
        while self.maze.maze_array[self.case_num_y][self.case_num_x] != "0":
            self.case_num_x = randint(1, 14)
            self.case_num_y = randint(1, 14)
            self.x = self.case_num_x * SPRITE_SIZE
            self.y = self.case_num_y * SPRITE_SIZE

        """To avoid tools'superposition"""
        self.maze.maze_array[self.case_num_y][self.case_num_x] = "T"

