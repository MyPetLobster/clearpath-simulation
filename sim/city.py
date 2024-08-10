import pygame as pg
from .settings import TILE_SIZE


class City:
    
    def __init__(self, grid_len_x, grid_len_y, width, height):
        self.grid_len_x = grid_len_x
        self.grid_len_y = grid_len_y
        self.width = width
        self.height = height
        
        self.city = self.create_city

    def create_city(self):
        city = []
        for grid_x in range(self.grid_len_x):
            city.append([])
            for grid_y in range(self.grid_len_y):
                city_tile = self.grid_to_city(grid_x, grid_y)
                city[grid_x].append(city_tile)

        return city
            
    def grid_to_city(self, grid_x, grid_y):
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        out = {
            "grid": [grid_x, grid_y],
            "cartesian_rect": rect
        }

        return out