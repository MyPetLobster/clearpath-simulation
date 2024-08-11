import pygame as pg
import random
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
FREQUENCY_OF_EVENTS = 0.01               # 10% chance of event happening every 5 seconds
VEHICLE_BASE_SPEED = 1                  # tiles per second
PEDESTRIAN_BASE_SPEED = 0.3               # tiles per second
EMERGENCY_VEHICLE_BASE_SPEED = 2        # tiles per second
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


# ----- City Grid Class -----
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
        crosswalks = [(11,10), (12,10), (11, 13), (12, 13), (10,11), (10, 12), (13, 11), (13, 12)]
        for crosswalk in crosswalks:
            self.grid[crosswalk[0]][crosswalk[1]] = 'crosswalk'
            
    def draw(self, win):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 'road' or self.grid[i][j] == 'occupied':
                    color = ROAD_COLOR
                elif self.grid[i][j] == 'sidewalk':
                    color = SIDEWALK_COLOR
                elif self.grid[i][j] == 'crosswalk':
                    color = CROSSWALK_COLOR
                else:
                    color = BLOCK_COLOR
                pg.draw.rect(win, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))




# ----- Vehicle Class -----
class Vehicle:
    def __init__(self, x, y, direction, grid, color=(255,255,255)):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = random.uniform(0.1, 1) * VEHICLE_BASE_SPEED
        self.grid = grid
        self.stopped = False

    def move(self):
        # Check ahead first to decide if the vehicle should stop
        if self.check_ahead():
            self.stopped = True
            return
        else:
            self.stopped = False      
        prev_x, prev_y = int(self.x), int(self.y)

        # Move the vehicle
        if self.direction == 'N':
            self.y -= self.speed
        elif self.direction == 'S':
            self.y += self.speed
        elif self.direction == 'E':
            self.x += self.speed
        elif self.direction == 'W':
            self.x -= self.speed

        current_x, current_y = int(self.x), int(self.y)
        print(f"Moving from ({prev_x}, {prev_y}) to ({current_x}, {current_y})")

        # Only reset the old position if the vehicle has fully left that tile
        if (prev_x != current_x or prev_y != current_y) and 0 <= prev_y < GRID_SIZE and 0 <= prev_x < GRID_SIZE:
            crosswalk_coords = [(11,10), (12,10), (11, 13), (12, 13), (10,11), (10, 12), (13, 11), (13, 12)]
            if (prev_x, prev_y) in crosswalk_coords:
                self.grid[prev_y][prev_x] = 'crosswalk'
            else:
                self.grid[prev_y][prev_x] = 'road'

        # Set grid to occupied for the new position if it's within the grid
        if 1 <= current_y < GRID_SIZE and 1 <= current_x < GRID_SIZE:   # Changed from 0 to 1 to fix negative indexing/'occupied' bug
            self.grid[current_y][current_x] = 'occupied'


    def check_ahead(self):
        next_x, next_y = int(self.x), int(self.y)
        if self.direction == 'N':
            next_y = int(self.y - 2)
        elif self.direction == 'S':
            next_y = int(self.y + 2)
        elif self.direction == 'E':
            next_x = int(self.x + 2)
        elif self.direction == 'W':
            next_x = int(self.x - 2)

        # Ensure next_x and next_y are within bounds before accessing the grid
        if 0 <= next_y < GRID_SIZE and 0 <= next_x < GRID_SIZE:
            print(f"Checking ahead to ({next_x}, {next_y}), grid value: {self.grid[next_y][next_x]}")
            if self.grid[next_y][next_x] == 'occupied':
                print(f"Vehicle at ({self.x}, {self.y}) is stopping")
                return True
            else:
                return False
        else:
            # Allow vehicles to move off the screen if they are at the grid boundary
            return False

    def draw(self, win):
        # Only draw if the vehicle is at least partially on screen
        if (0 <= int(self.x * TILE_SIZE) < WIDTH and 
            0 <= int(self.y * TILE_SIZE) < HEIGHT):
            pg.draw.rect(win, self.color, (int(self.x * TILE_SIZE), int(self.y * TILE_SIZE), TILE_SIZE, TILE_SIZE))
    
    def is_off_screen(self):
        return self.x < 0 or self.x > GRID_SIZE or self.y < 0 or self.y > GRID_SIZE





# ----- Pedestrian Class -----
class Pedestrian:
    def __init__(self, x, y, speed=PEDESTRIAN_BASE_SPEED):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        pass

    def draw(self, win):
        pass


# ----- Emergency Vehicle Class -----



# ----- Traffic Light Class -----
class TrafficLight:
    def __init__(self, x, y, state='RED'):
        self.x = x
        self.y = y
        self.state = state
        self.timer = 0


    def update(self, grid):
        self.timer += 1
        if self.state == 'GREEN' and self.timer >= GREEN_LIGHT_DURATION * 60:
            self.state = 'YELLOW'
            self.timer = 0
            # self.mark_crosswalks(grid, True)
        elif self.state == 'YELLOW' and self.timer >= YELLOW_LIGHT_DURATION * 60:
            self.state = 'RED'
            self.timer = 0
            # self.mark_crosswalks(grid, True)
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


# ----- Main Simulation Class -----
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
        self.vehicles = []

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
            light.update(self.city.grid)

        # Update vehicles
        vehicles_to_remove = []
        for vehicle in self.vehicles:
            vehicle.move()
            if vehicle.is_off_screen():
                vehicles_to_remove.append(vehicle)

        # Remove off-screen vehicles
        for vehicle in vehicles_to_remove:
            self.vehicles.remove(vehicle)

        # Add new vehicles
        if random.random() < FREQUENCY_OF_EVENTS:
            self.add_vehicle()

    def add_vehicle(self):
        direction = random.choice(['N', 'S', 'E', 'W'])
        if direction == 'N':
            x = 12
            y = 23
        elif direction == 'S':
            x = 11
            y = 0
        elif direction == 'E':
            x = 0
            y = 12
        else:
            x = 23
            y = 11

        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.vehicles.append(Vehicle(x, y, direction, self.city.grid, color))


    def draw(self):
        self.city.draw(self.win)
        # Draw the split tiles
        for (x, y) in self.split_tiles:
            self.draw_split_tile(x, y)

        for light in self.traffic_lights:
            light.draw(self.win)

        for vehicle in self.vehicles:
            vehicle.draw(self.win)



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
        return RED_LIGHT       # Fallback color, should never reach here
    


if __name__ == "__main__":
    sim = Simulation(WIN, clock)
    sim.run()
