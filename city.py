import pygame as pg
from config import ROAD_COLOR, SIDEWALK_COLOR, BLOCK_COLOR, CROSSWALK_COLOR, TILE_SIZE, YELLOW_STRIPE, CROSSWALK_TILES, INTERSECTION_TILES


class CityGrid:
    """
    Attributes:
        - grid_size (int): The size of the grid
        - grid (list): 2D list representing the city grid
        - crosswalks (list): List of crosswalk coordinates
        - traffic_lights (list): List of traffic lights in the city
        - active_emergency_vehicles (list): List of active emergency vehicles in the city

    Methods:
        - create_grid: Creates a grid of size grid_size x grid_size
        - set_city_elements: Sets up the roads, sidewalks, and crosswalks
        - draw: Draws the city grid on the screen
        - add_traffic_light: Adds a traffic light to the
    """
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.create_grid()
        self.crosswalks = CROSSWALK_TILES["EW"] + CROSSWALK_TILES["NS"]
        self.traffic_lights = []
        self.active_emergency_vehicles = []
    
    def create_grid(self):
        """
        Creates an empty grid of the given size.

        Returns:
            list: 2D list representing the city grid, initialized with 'empty' values.
        """
        return [['empty' for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def set_city_elements(self):
        """
        Sets up the roads and sidewalks on the city grid.
        """
        self.set_roads()
        self.set_sidewalks()

    def set_roads(self):
        """
        Marks the road tiles on the grid.
        """
        for i in range(self.grid_size):
            self.grid[11][i] = 'road'
            self.grid[i][11] = 'road'
            self.grid[12][i] = 'road'
            self.grid[i][12] = 'road'

    def set_sidewalks(self):
        """
        Marks the sidewalk tiles on the grid.
        """
        for i in range(self.grid_size):
            self.grid[10][i] = 'sidewalk'
            self.grid[i][10] = 'sidewalk'
            self.grid[13][i] = 'sidewalk'
            self.grid[i][13] = 'sidewalk'

    def draw(self, win):
        """
        Draws the city grid on the screen.

        Args:
            win (Surface): The pygame window to draw on.
        """
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.draw_tile(win, i, j)

    def draw_tile(self, win, i, j):
        """
        Draws an individual tile on the grid.

        Args:
            win (Surface): The pygame window to draw on.
            i (int): The row index of the tile.
            j (int): The column index of the tile.
        """
        if self.grid[i][j] in ['road', 'occupied']:
            color = ROAD_COLOR
        elif self.grid[i][j] == 'sidewalk':
            color = SIDEWALK_COLOR
        else:
            color = BLOCK_COLOR

        # Use crosswalk color if the tile is a crosswalk
        if (i, j) in self.crosswalks:
            color = CROSSWALK_COLOR

        pg.draw.rect(win, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw yellow line between road tiles, except at intersections
        if self.grid[i][j] in ['road', 'occupied'] and (i, j) not in self.crosswalks and (i, j) not in INTERSECTION_TILES:
            self.draw_yellow_stripe(win, i, j)

    def draw_yellow_stripe(self, win, i, j):
        """
        Draws a yellow stripe on the road tiles.

        Args:
            win (Surface): The pygame window to draw on.
            i (int): The row index of the tile.
            j (int): The column index of the tile.
        """
        if i == 12:  # Horizontal roads (between rows 11 and 12)
            pg.draw.line(win, YELLOW_STRIPE, (j * TILE_SIZE, i * TILE_SIZE), ((j + 1) * TILE_SIZE, i * TILE_SIZE))
        if j == 12:  # Vertical roads (between columns 11 and 12)
            pg.draw.line(win, YELLOW_STRIPE, (j * TILE_SIZE, i * TILE_SIZE), (j * TILE_SIZE, (i + 1) * TILE_SIZE))
                        
    def add_traffic_light(self, traffic_light):
        """
        Adds a traffic light to the city grid.

        Args:
            traffic_light (TrafficLight): The traffic light to add.
        """
        self.traffic_lights.append(traffic_light)