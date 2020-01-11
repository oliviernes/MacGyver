import pygame
import random
from random import randint
from constants import *

class Homepage:
    """Show homepage"""

    def __init__(self, homepage):
        self.homepage = homepage

    def show(self, window):
        page = pygame.image.load(self.homepage).convert()
        window.blit(page, (0, 0))
        
class Map:
    """build the map from map*.txt files"""

    def __init__(self, map_file):
        """Generates an array in order to display the maze"""
        self.map_file = map_file

        with open(self.map_file, "r") as maze_file:
            maze_list = []
            for line in maze_file:
                line_level = []
                for sprite in line:
                    if sprite != '\n':
                        line_level.append(sprite)
                maze_list.append(line_level)
            self.maze_array = maze_list

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
        text1 = font.render(msg, True, (255, 255, 255), (0, 0, 0))
        window.blit(text1, (0, SPRITE_SIZE * SPRITES_NUMBER))

    def warden_asleep_info(self, window, msg, color_text):
        font = pygame.font.Font(None, 35)
        text2 = font.render(msg, True, color_text, (0, 0, 0))
        window.blit(text2, (0, SPRITE_SIZE * (SPRITES_NUMBER + 1)))
                
class BaseSprite():
    """Base class for objects"""
    def __init__(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        
    def position(self, case_number_x = 0, case_number_y = 0):
        """return object's position"""
        self.case_number_x = case_number_x
        self.case_number_y = case_number_y
        self.x = self.case_number_x * SPRITE_SIZE
        self.y = self.case_number_y * SPRITE_SIZE
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
            if self.case_number_x < (SPRITES_NUMBER - 1):
                if self.maze.maze_array[self.case_number_y][self.case_number_x + 1] != "m":
                    self.case_number_x += 1
                    self.x = self.case_number_x * SPRITE_SIZE

        if direction == "left":
            if self.case_number_x > 0:
                if self.maze.maze_array[self.case_number_y][self.case_number_x - 1] != "m":
                    self.case_number_x -= 1
                    self.x = self.case_number_x * SPRITE_SIZE
                    
        if direction == "up":
            if self.case_number_y > 0:
                if self.maze.maze_array[self.case_number_y - 1][self.case_number_x] != "m":
                    self.case_number_y -= 1
                    self.y = self.case_number_y * SPRITE_SIZE
                    
        if direction == "down":
            if self.case_number_y < (SPRITES_NUMBER - 1):
                if self.maze.maze_array[self.case_number_y + 1][self.case_number_x] != "m":
                    self.case_number_y += 1
                    self.y = self.case_number_y * SPRITE_SIZE

    def check_tools(self, list_tool, grabbed_tools):
        """bug of the sound_tools: Fatal Python error: take_gil: NULL tstate"""
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
        while self.maze.maze_array[self.case_number_y][self.case_number_x] != "0":
            self.case_number_x = randint(1, 14)
            self.case_number_y= randint(1, 14)
            self.x = self.case_number_x * SPRITE_SIZE
            self.y = self.case_number_y * SPRITE_SIZE        

        """To avoid tools'superposition"""
        self.maze.maze_array[self.case_number_y][self.case_number_x] = "T"

                    
