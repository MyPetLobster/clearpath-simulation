import pygame as pg
import sys




# Set up colors
ROAD_COLOR = (40, 40, 40)
SIDEWALK_COLOR = (90, 90, 90)
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
WIDTH, HEIGHT = 800, 600    # pixels
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
            self.grid[11][i] = 1
            self.grid[i][11] = 1
            self.grid[12][i] = 1
            self.grid[i][12] = 1

        # Set up sidewalks
        for i in range(self.grid_size):
            self.grid[10][i] = 2
            self.grid[i][10] = 2
            self.grid[13][i] = 2
            self.grid[i][13] = 2

    def draw(self, win):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 1:
                    color = ROAD_COLOR
                elif self.grid[i][j] == 2:
                    color = SIDEWALK_COLOR
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

# class Vehicle:
#     def __init__(self, x, y, speed):
#         self.x = x
#         self.y = y
#         self.speed = speed
#         self.direction = 'EAST'

#     def move(self):
#         if self.direction == 'EAST':
#             self.x += self.speed
#         elif self.direction == 'WEST':
#             self.x -= self.speed
#         elif self.direction == 'NORTH':
#             self.y -= self.speed
#         elif self.direction == 'SOUTH':
#             self.y += self.speed

#     def draw(self, win):
#         pg.draw.rect(win, (255, 255, 255), (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


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




if __name__ == "__main__":
    sim = Simulation(WIN, clock)
    sim.run()
