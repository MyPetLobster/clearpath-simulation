import random
import pygame as pg

from config import VEHICLE_BASE_SPEED, GRID_SIZE, TILE_SIZE, WIDTH, HEIGHT



class Vehicle:
    """
    A class to represent a vehicle in the simulation.
    
    Attributes:
        - x (float): The x-coordinate of the vehicle
        - y (float): The y-coordinate of the vehicle
        - direction (str): The direction the vehicle is traveling (N, S, E, W)
        - color (tuple): The color of the vehicle
        - speed (float): The speed of the vehicle
        - city (CityGrid): The city grid the vehicle is traveling on
        - grid (list): The grid of the city
        - stopped (bool): Whether the vehicle is stopped
        - in_intersection (bool): Whether the vehicle is in the intersection
    
    Methods:
        - move: Move the vehicle in the direction it is traveling
        - check_ahead: Check if the next tile is occupied or if the vehicle should stop
        - get_relevant_light: Get the relevant traffic light for the vehicle's direction
        - draw: Draw the vehicle on the screen
        - is_off_screen: Check if the vehicle is off the screen
    """

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
        """
        Move the vehicle based on its direction and speed, updating its position on the grid.

        This method checks the traffic light ahead to determine if the vehicle should stop.
        If movement is allowed, it updates the vehicle's position, marks the grid, and checks
        if the vehicle is within an intersection.

        Updates:
            - `self.stopped`: Whether the vehicle is stopped.
            - `self.in_intersection`: Whether the vehicle is within the intersection.
        
        Returns:
            None
        """
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
        """
        Check if the vehicle should stop based on the traffic light ahead and the next tile.
        
        Args:
            - relevant_light (TrafficLight): The traffic light relevant to the vehicle's direction.
            
        Returns:
            - bool: Whether the vehicle should stop.
        """
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
        """
        Get the relevant traffic light for the vehicle's direction.
        
        Args:
            - traffic_lights (list): List of traffic lights in the simulation.
            
        Returns:
            - TrafficLight: The relevant traffic light for the vehicle's direction.
        """
        if self.direction == 'N':
            return next((light for light in traffic_lights if light.x == 13 and light.y == 14), None)
        elif self.direction == 'S':
            return next((light for light in traffic_lights if light.x == 10 and light.y == 9), None)
        elif self.direction == 'E':
            return next((light for light in traffic_lights if light.x == 9 and light.y == 10), None)
        elif self.direction == 'W':
            return next((light for light in traffic_lights if light.x == 14 and light.y == 13), None)


    def draw(self, win):
        """
        Draw the vehicle on the screen.

        Args:
            - win (pygame.Surface): The window to draw the vehicle on.

        Returns:
            None
        """
        # Only draw if the vehicle is at least partially on screen
        if (0 <= int(self.x * TILE_SIZE) < WIDTH and 
            0 <= int(self.y * TILE_SIZE) < HEIGHT):
            pg.draw.rect(win, self.color, (int(self.x * TILE_SIZE), int(self.y * TILE_SIZE), TILE_SIZE, TILE_SIZE))
    
    def is_off_screen(self):
        return self.x < 0 or self.x > GRID_SIZE or self.y < 0 or self.y > GRID_SIZE
    


class EmergencyVehicle(Vehicle):
    def __init__(self, x, y, direction, city, code3, color=(255,255,255)):
        super().__init__(x, y, direction, city, color)      # initialize the vehicle with the same attributes
        self.speed = random.uniform(0.1, 1) * VEHICLE_BASE_SPEED * 1.3    # increase the speed of the emergency vehicle
        self.code3 = code3    # whether the vehicle is in code 3 mode (lights and sirens)

    def check_ahead(self, relevant_light):
        """
        Check if the vehicle should stop based on the traffic light ahead and the next tile.
        ** Emergency vehicles will ignore traffic lights if running code 3. **

        Args:
            - relevant_light (TrafficLight): The traffic light relevant to the vehicle's direction.

        Returns:
            - bool: Whether the vehicle should stop.
        """
        if self.code3:
            print("Ignoring traffic light!")
            return False
        else:
            return super().check_ahead(relevant_light)

    def flash_lights(self):
        """This function makes the color of the emergency vehicle cycle between red, white, and blue"""
        if self.color == (255, 0, 0):
            self.color = (255, 255, 255)
        elif self.color == (255, 255, 255):
            self.color = (0, 0, 255)
        else:
            self.color = (255, 0, 0)



def generate_emergency_vehicle():
    """
    Generate an emergency vehicle with a random starting position, direction

    Returns:
        - tuple: The x-coordinate, y-coordinate, direction, and color of the emergency vehicle.
    """
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

    is_code3 = random.random() < 0.5       # 50% chance of generating a vehicle in code 3 mode
    
    print("is_code3:", is_code3)

    return x, y, direction, is_code3


def generate_vehicle():
    """
    Generate a vehicle with a random starting position, direction, and color.

    Returns:
        - tuple: The x-coordinate, y-coordinate, direction, and color of the vehicle.
    """
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