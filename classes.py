import pygame
import random
from random import randint
from constants import *

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

class Tools(BaseSprite):
    """to instance and display MacGyver's objects"""

    def __init__(self, maze, image):
        super().__init__(image)
        self.maze = maze       
        
    def place_item(self, maze):
        while self.maze.maze_array[self.case_number_y][self.case_number_x] != "0":
            self.case_number_x = randint(1, 14)
            self.case_number_y= randint(1, 14)
            self.x = self.case_number_x * SPRITE_SIZE
            self.y = self.case_number_y * SPRITE_SIZE        
