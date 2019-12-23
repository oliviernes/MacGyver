import pygame
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
                elif sprite == "0":
                    window.blit(floor, (x, y))
                    
