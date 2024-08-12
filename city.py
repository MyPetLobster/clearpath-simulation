import pygame as pg

from config import ROAD_COLOR, SIDEWALK_COLOR, BLOCK_COLOR, CROSSWALK_COLOR, TILE_SIZE


class CityGrid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.create_grid()
        self.crosswalks = [(11,10), (12,10), (11, 13), (12, 13), (10,11), (10, 12), (13, 11), (13, 12)]
        self.traffic_lights = []
    
    def create_grid(self):
        # Create a grid of size grid_size x grid_size 
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        return grid

    def set_city_elements(self):
        # Set up roads
        for i in range(self.grid_size):
            self.grid[11][i] = 'road'
            self.grid[i][11] = 'road'
            self.grid[12][i] = 'road'
            self.grid[i][12] = 'road'

        # Set up sidewalks
        for i in range(self.grid_size):
            self.grid[10][i] = 'sidewalk'
            self.grid[i][10] = 'sidewalk'
            self.grid[13][i] = 'sidewalk'
            self.grid[i][13] = 'sidewalk'

        # Set up crosswalks

        for crosswalk in self.crosswalks:
            self.grid[crosswalk[0]][crosswalk[1]] = 'crosswalk'
            
    def draw(self, win):
        # Draw the grid on the screen
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 'road' or self.grid[i][j] == 'occupied':
                    color = ROAD_COLOR
                elif self.grid[i][j] == 'sidewalk':
                    color = SIDEWALK_COLOR
                else:
                    color = BLOCK_COLOR
                
                # Decouple name and color for crosswalks. Need to use "occupied" in crosswalk tiles to control intersection
                if (i, j) in self.crosswalks:
                    color = CROSSWALK_COLOR

                pg.draw.rect(win, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
    def add_traffic_light(self, traffic_light):
        self.traffic_lights.append(traffic_light)


