import pygame as pg
import sys

# Set up colors
ROAD_COLOR = (40, 40, 40)
SIDEWALK_COLOR = (90, 90, 90)
CROSSWALK_COLOR = (255, 255, 255)
RED_LIGHT = (255, 0, 0)
GREEN_LIGHT = (0, 255, 0)
YELLOW_LIGHT = (255, 255, 0)
YELLOW_STRIPE = (225, 225, 15)
BLOCK_COLOR = (0, 0, 0)

# Other Global Variables
NUMBER_OF_CARS = 10
NUMBER_OF_PEDESTRIANS = 10
NUMBER_OF_EMERGENCY_VEHICLES = 2
FREQUENCY_OF_EVENTS = 0.1               # 10% chance of event happening every 5 seconds
VEHICLE_BASE_SPEED = 8                  # pixels per second
PEDESTRIAN_BASE_SPEED = 2               # pixels per second
EMERGENCY_VEHICLE_BASE_SPEED = 10       # pixels per second
GREEN_LIGHT_DURATION = 10               # seconds
YELLOW_LIGHT_DURATION = 3               # seconds
RED_LIGHT_DURATION = 13                 # seconds

# Settings
TILE_SIZE = 32              # pixels
WIDTH, HEIGHT = 768, 768    # pixels
GRID_SIZE = 24              # tiles

# Initialize pygame
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ClearPath Simulation")
clock = pg.time.Clock()

class CityGrid:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = self.create_grid()

    def create_grid(self):
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
        crosswalks = [(11,10), (12,10), (10,11), (10, 12), (13, 11), (13, 12), (11, 13), (12, 13)]
        for crosswalk in crosswalks:
            self.grid[crosswalk[0]][crosswalk[1]] = 'crosswalk'

    def draw(self, win):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 'road':
                    color = ROAD_COLOR
                elif self.grid[i][j] == 'sidewalk':
                    color = SIDEWALK_COLOR
                elif self.grid[i][j] == 'crosswalk':
                    color = CROSSWALK_COLOR
                else:
                    color = BLOCK_COLOR
                pg.draw.rect(win, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

class TrafficLight:
    def __init__(self, x, y, state='RED'):
        self.x = x
        self.y = y
        self.state = state
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.state == 'GREEN' and self.timer >= GREEN_LIGHT_DURATION * 60:
            self.state = 'YELLOW'
            self.timer = 0
        elif self.state == 'YELLOW' and self.timer >= YELLOW_LIGHT_DURATION * 60:
            self.state = 'RED'
            self.timer = 0
        elif self.state == 'RED' and self.timer >= RED_LIGHT_DURATION * 60:
            self.state = 'GREEN'
            self.timer = 0

    def draw(self, win):
        if self.state == 'RED':
            color = RED_LIGHT
        elif self.state == 'YELLOW':
            color = YELLOW_LIGHT
        else:
            color = GREEN_LIGHT
        pg.draw.rect(win, color, (self.y * TILE_SIZE, self.x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

class Simulation:
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.city = CityGrid(GRID_SIZE)
        self.city.set_city_elements()
        self.traffic_lights = [
            TrafficLight(10, 9, 'GREEN'), TrafficLight(10, 14, 'GREEN'), TrafficLight(13, 9, 'GREEN'), TrafficLight(13, 14, 'GREEN'),
            TrafficLight(9, 10), TrafficLight(14, 10), TrafficLight(9, 13), TrafficLight(14, 13)
            ]
        self.split_tiles = [(10,10), (10,13), (13,10), (13,13)]

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(60)
        pg.quit()

    def update(self):
        for light in self.traffic_lights:
            light.update()

    def draw(self):
        self.city.draw(self.win)

        for light in self.traffic_lights:
            light.draw(self.win)

        # Draw the split tiles
        for (x, y) in self.split_tiles:
            self.draw_split_tile(x, y)

    def draw_split_tile(self, x, y):
        # Find the adjacent lights and match their colors

        north_south_color = self.get_light_color(9, 10) 
        east_west_color = self.get_light_color(10,9)

        top_left = (x * TILE_SIZE, y * TILE_SIZE)
        top_right = ((x + 1) * TILE_SIZE, y * TILE_SIZE)
        bottom_left = (x * TILE_SIZE, (y + 1) * TILE_SIZE)
        bottom_right = ((x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE)

        # Draw the two triangles for each corner of intersection
        if x == 10 and y == 10:
            pg.draw.polygon(self.win, north_south_color, [top_left, top_right, bottom_right])
            pg.draw.polygon(self.win, east_west_color, [top_left, bottom_left, bottom_right])
        elif x == 13 and y == 10:
            pg.draw.polygon(self.win, north_south_color, [top_left, top_right, bottom_left])
            pg.draw.polygon(self.win, east_west_color, [top_right, bottom_left, bottom_right])
        elif x == 13 and y == 13:
            pg.draw.polygon(self.win, east_west_color, [top_left, top_right, bottom_right])
            pg.draw.polygon(self.win, north_south_color, [top_left, bottom_left, bottom_right])
        elif x == 10 and y == 13:
            pg.draw.polygon(self.win, east_west_color, [top_left, top_right, bottom_left])
            pg.draw.polygon(self.win, north_south_color, [top_right, bottom_left, bottom_right])
    


    def get_light_color(self, x, y):
        for light in self.traffic_lights:
            if light.x == x and light.y == y:
                if light.state == 'RED':
                    return RED_LIGHT
                elif light.state == 'YELLOW':
                    return YELLOW_LIGHT
                elif light.state == 'GREEN':
                    return GREEN_LIGHT
        return SIDEWALK_COLOR  # Default to sidewalk color if no adjacent light

if __name__ == "__main__":
    sim = Simulation(WIN, clock)
    sim.run()
