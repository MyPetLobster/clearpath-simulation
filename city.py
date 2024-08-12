import pygame as pg

from config import ROAD_COLOR, SIDEWALK_COLOR, BLOCK_COLOR, CROSSWALK_COLOR, TILE_SIZE, YELLOW_STRIPE


class CityGrid:
    """
    Class to represent the city grid

    Attributes:
        - grid_size (int): The size of the grid
        - grid (list): 2D list representing the city grid
        - crosswalks (list): List of crosswalk coordinates
        - traffic_lights (list): List of traffic lights in the city

    Methods:
        - create_grid: Creates a grid of size grid_size x grid_size
        - set_city_elements: Sets up the roads, sidewalks, and crosswalks
        - draw: Draws the city grid on the screen
        - add_traffic_light: Adds a traffic light to the
    """
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.create_grid()
        self.crosswalks = [(11,10), (12,10), (11, 13), (12, 13), (10,11), (10, 12), (13, 11), (13, 12)]
        self.traffic_lights = []
    
    def create_grid(self):
        """
        Creates a grid of size grid_size x grid_size
        
        Returns:
            - list: 2D list representing the city grid
        """
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        return grid

    def set_city_elements(self):
        """
        Sets up the roads, sidewalks, and crosswalks on the city grid
        """
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
        """
        Draws the city grid on the screen

        Args:
            - win (Surface): The pygame window to draw on

        Returns:
            None
        """
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

                # Draw yellow line between road tiles
                if self.grid[i][j] == 'road':
                    # Exclude the intersection tiles
                    if (i, j) not in [(11, 11), (11, 12), (12, 11), (12, 12)]:
                        # Horizontal roads (between rows 11 and 12)
                        if i == 12:
                            pg.draw.line(win, YELLOW_STRIPE, (j * TILE_SIZE, i * TILE_SIZE), ((j + 1) * TILE_SIZE, i * TILE_SIZE))
                        # Vertical roads (between columns 11 and 12)
                        if j == 12:
                            pg.draw.line(win, YELLOW_STRIPE, (j * TILE_SIZE, i * TILE_SIZE), (j * TILE_SIZE, (i + 1) * TILE_SIZE))
                        
    def add_traffic_light(self, traffic_light):
        """
        Adds a traffic light to the city grid

        Args:
            - traffic_light (TrafficLight): The traffic light to add

        Returns:
            None
        """
        self.traffic_lights.append(traffic_light)


