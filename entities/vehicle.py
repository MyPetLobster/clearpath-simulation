import random
import pygame as pg

from config import VEHICLE_BASE_SPEED, GRID_SIZE, TILE_SIZE, WIDTH, HEIGHT



class Vehicle:
    def __init__(self, x, y, direction, city, color=(255,255,255)):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = random.uniform(0.1, 1) * VEHICLE_BASE_SPEED
        self.city = city
        self.grid = city.grid
        self.stopped = False
        self.in_intersection = False

    def move(self):
        # Get the relevant traffic light for the vehicle's direction
        relevant_light = self.get_relevant_light(self.city.traffic_lights)
        
        # Check ahead to decide if the vehicle should stop
        if self.check_ahead(relevant_light):
            self.stopped = True
            return
        else:
            self.stopped = False      

        # Save the previous position
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

        # Update the grid to reflect the new position
        current_x, current_y = int(self.x), int(self.y)

        # Only reset the old position if the vehicle has fully left that tile
        if (prev_x != current_x or prev_y != current_y) and 0 <= prev_y < GRID_SIZE and 0 <= prev_x < GRID_SIZE:
            self.grid[prev_y][prev_x] = 'road'

        # Set grid to occupied for the new position if it's within the grid
        if 1 <= current_y < GRID_SIZE and 1 <= current_x < GRID_SIZE:  # Changed from 0 to 1 to fix negative indexing/'occupied' bug
            self.grid[current_y][current_x] = 'occupied'

        # Check if vehicle has entered or exited the intersection
        if self.direction in ['N', 'S'] and 10 <= self.y <= 13:
            self.in_intersection = True
        elif self.direction in ['E', 'W'] and 10 <= self.x <= 13:
            self.in_intersection = True
        else:
            self.in_intersection = False

    def check_ahead(self, relevant_light):
        # Check if the next tile is occupied
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
            # If the next tile is occupied, stop the vehicle
            if self.grid[next_y][next_x] == 'occupied':
                return True

        # Check for yellow light
        if relevant_light and relevant_light.state == 'YELLOW':
            yellow_duration = relevant_light.get_yellow_duration()
            if yellow_duration > 1.5 and not self.in_intersection:
                return True  # Stop for yellow light if it's been on for more than 1.5 seconds and not in intersection

        # If we've reached this point, there's no reason to stop
        return False

    def get_relevant_light(self, traffic_lights):
        if self.direction == 'N':
            return next((light for light in traffic_lights if light.x == 13 and light.y == 14), None)
        elif self.direction == 'S':
            return next((light for light in traffic_lights if light.x == 10 and light.y == 9), None)
        elif self.direction == 'E':
            return next((light for light in traffic_lights if light.x == 9 and light.y == 10), None)
        elif self.direction == 'W':
            return next((light for light in traffic_lights if light.x == 14 and light.y == 13), None)


    def draw(self, win):
        # Only draw if the vehicle is at least partially on screen
        if (0 <= int(self.x * TILE_SIZE) < WIDTH and 
            0 <= int(self.y * TILE_SIZE) < HEIGHT):
            pg.draw.rect(win, self.color, (int(self.x * TILE_SIZE), int(self.y * TILE_SIZE), TILE_SIZE, TILE_SIZE))
    
    def is_off_screen(self):
        return self.x < 0 or self.x > GRID_SIZE or self.y < 0 or self.y > GRID_SIZE
    


def generate_vehicle():
    # Pick a random direction/starting point for the vehicle
    direction = random.choice(['N', 'S', 'E', 'W'])
    if direction == 'N':
        x, y = 12, 23
    elif direction == 'S':
        x, y = 11, 0
    elif direction == 'E':
        x, y = 0, 12
    else:
        x, y = 23, 11

    # Choose a random color for the vehicle
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    return x, y, direction, color