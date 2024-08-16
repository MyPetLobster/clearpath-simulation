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
        - pulled_over (bool): Whether the vehicle has pulled over for an emergency vehicle
        - at_red_light (bool): Whether the vehicle is at a red light
        - in_intersection (bool): Whether the vehicle is within the intersection
        - four_way_timer (int): Timer for the 4-way stop
        - four_way_state (str): State of the 4-way stop
        - wait_time (int): Time the vehicle has been waiting at a red light
    
    Methods:
        - move: Move the vehicle in the direction it is traveling
        - check_ahead: Check if the next tile is occupied or if the vehicle should stop
        - draw: Draw the vehicle on the screen
        - is_off_screen: Check if the vehicle is off the screen
    """

    def __init__(self, x, y, direction, city, color=(255,255,255)):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = random.uniform(0.3, 0.7) * VEHICLE_BASE_SPEED
        self.city = city
        self.grid = city.grid
        self.stopped = False
        self.pulled_over = False
        self.at_red_light = False
        self.in_intersection = False
        self.four_way_timer = 0  
        self.four_way_state = "approaching"  
        self.wait_time = 0  

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
        # Check if the vehicle is pulled over for emergency vehicle
        if self.pulled_over:
            return

        # Check ahead for occupied tiles or red lights
        if self.check_ahead():
            self.stopped = True
            return
        else:
            self.stopped = False      

        # Save the previous position
        prev_x, prev_y = int(self.x), int(self.y)

        # Move the vehicle based on its direction and speed
        if self.direction == 'N':
            self.y -= self.speed
        elif self.direction == 'S':
            self.y += self.speed
        elif self.direction == 'E':
            self.x += self.speed
        elif self.direction == 'W':
            self.x -= self.speed

        # Update the grid to reflect the new position and check if the vehicle is in the intersection
        current_x, current_y = int(self.x), int(self.y)
        self.update_vehicle_grid_positions(prev_x, prev_y, current_x, current_y)
        self.in_intersection = self.check_if_in_intersection()

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

    def check_ahead(self):
        """
        Check if the vehicle should stop based on the traffic light ahead and the next tile.
        
        Args:
            None
            
        Returns:
            - bool: Whether the vehicle should stop.
        """
        # Continue without checking if in intersection
        if self.in_intersection or self.four_way_state == "proceeding":
            return False

        next_x, next_y = int(self.x), int(self.y)

        # Check if either of the next two tiles are occupied
        for i in range(1, 3):
            if self.direction == 'N':
                next_y = int(self.y - i)
            elif self.direction == 'S':
                next_y = int(self.y + i)
            elif self.direction == 'E':
                next_x = int(self.x + i)
            elif self.direction == 'W':
                next_x = int(self.x - i)

            # Ensure next_x and next_y are within bounds before accessing the grid
            if 0 <= next_y < GRID_SIZE and 0 <= next_x < GRID_SIZE:
                # If the next tile is occupied, stop the vehicle
                if self.grid[next_y][next_x] == 'occupied' or self.grid[next_y][next_x] == '4_way_red' or self.grid[next_y][next_x] == 'red_light':
                    return True

                if self.grid[next_y][next_x] == '4_way_red':
                    if self.four_way_state == "approaching": 
                        self.four_way_state = "waiting" 
                        self.four_way_timer += 1
                        return True
                    if self.four_way_state == "waiting":
                        self.four_way_timer += 1
                        return True
            
        # If we've reached this point, there's no reason to stop
        return False
    
    def look_both_ways(self):
        """
        Checks for oncoming emergency vehicles to see if vehicle can safely enter intersection at 4-way stop.

        Returns:
            - bool: Whether the vehicle can proceed.
        """
        emergency_vehicles = self.city.active_emergency_vehicles

        for vehicle in emergency_vehicles:
            if self.direction == 'N' or self.direction == 'S':
                if vehicle.direction == 'E' or vehicle.direction == 'W':
                    return False
            elif self.direction == 'E' or self.direction == 'W':
                if vehicle.direction == 'N' or vehicle.direction == 'S':
                    return False
        return True
    
    def check_behind(self, vehicles):
        """
        Check 5 tiles behind and 2 tiles ahead of the vehicle to check for oncoming emergency vehicles in code 3 mode.
        
        Args:
            - vehicles (list): List of vehicles in the simulation.
            
        Modifies:
            - self.stopped: Whether the vehicle should stop.
            - self.x, self.y: The position of the vehicle.
        """
        if self.pulled_over:
            # If already pulled over, check if it's safe to merge back.
            self.merge(vehicles)
        else:
            # Check the area behind and ahead for emergency vehicles
            for vehicle in vehicles:
                if isinstance(vehicle, EmergencyVehicle):
                    if self.is_emergency_vehicle_in_range(vehicle):
                        self.pull_over()
                        self.stopped = True
                        return
                    
    def is_emergency_vehicle_in_range(self, vehicle):
        """
        Determine if an emergency vehicle is within the check range.
        
        Args:
            vehicle (Vehicle): The vehicle to check.
            
        Returns:
            bool: True if the vehicle is within range, False otherwise.
        """
        if self.direction == vehicle.direction:
            in_range = (
                (self.direction == "N" and self.y - 2 <= vehicle.y <= self.y + 5) or
                (self.direction == "S" and self.y - 5 <= vehicle.y <= self.y + 2) or
                (self.direction == "E" and self.x - 5 <= vehicle.x <= self.x + 2) or
                (self.direction == "W" and self.x - 2 <= vehicle.x <= self.x + 5)
            )
            if in_range:
                return True
        return False

    def pull_over(self):
        """
        Move the vehicle to the right side of the road if there's an emergency vehicle approaching.

        Modifies:
            - self.stopped: Whether the vehicle is stopped.
            - self.pulled_over: Whether the vehicle has pulled over.
            - self.x, self.y: The position of the vehicle.
        """
        # Do not pull over if within the intersection
        if self.in_intersection: 
            return
        
        # Ensure the vehicle stops
        self.stopped = True
        self.pulled_over = True

        # Save the previous position to keep it marked as occupied
        prev_x, prev_y = int(self.x), int(self.y)

        # Move the vehicle to the right side of the road
        if self.direction == 'N':
            self.x += 1  # Move right
            if self.x == 11 or self.x == 12:        # Check if vehicle is in intersection
                self.y -= 2 # Move up
        elif self.direction == 'S':
            self.x -= 1  # Move left
            if self.x == 11 or self.x == 12:
                self.y += 2 # Move down
        elif self.direction == 'E':
            self.y += 1  # Move up
            if self.y == 11 or self.y == 12:
                self.x += 2 # Move right
        elif self.direction == 'W':
            self.y -= 1  # Move down
            if self.y == 11 or self.y == 12:
                self.x -= 2 # Move left

        # Mark the old position as occupied
        if 0 <= prev_y < GRID_SIZE and 0 <= prev_x < GRID_SIZE:
            if self.grid[prev_y][prev_x] != '4_way_red':
                self.grid[prev_y][prev_x] = 'occupied'

    def merge(self, vehicles):
        """
        Merge the vehicle back into the road after pulling over.

        Args:
            - vehicles (list): List of vehicles in the simulation.

        Modifies:
            - self.stopped: Whether the vehicle is stopped.
            - self.pulled_over: Whether the vehicle has pulled over.
            - self.x, self.y: The position of the vehicle.
        """
        # Check if there's still an emergency vehicle within the danger zone
        for vehicle in vehicles:
            if isinstance(vehicle, EmergencyVehicle):
                if self.is_emergency_vehicle_in_range(vehicle):
                    return  # Stay pulled over if the emergency vehicle is still nearby

        # Define next_x and next_y based on current position
        next_x, next_y = self.x, self.y

        # Check the next space before merging back, with boundary checks
        if self.direction == 'N':
            if int(self.y) - 2 >= 0 and self.grid[int(self.y - 2)][int(self.x)] == 'occupied':
                return
            if int(self.y) - 1 >= 0 and self.grid[int(self.y - 1)][int(self.x)] == 'occupied':
                return
            next_x -= 1  # Move back to the left
        elif self.direction == 'S':
            if int(self.y) + 2 < GRID_SIZE and self.grid[int(self.y + 2)][int(self.x)] == 'occupied':
                return
            if int(self.y) + 1 < GRID_SIZE and self.grid[int(self.y + 1)][int(self.x)] == 'occupied':
                return
            next_x += 1  # Move back to the right
        elif self.direction == 'E':
            if int(self.x) + 2 < GRID_SIZE and self.grid[int(self.y)][int(self.x + 2)] == 'occupied':
                return
            if int(self.x) + 1 < GRID_SIZE and self.grid[int(self.y)][int(self.x + 1)] == 'occupied':
                return
            next_y -= 1  # Move back down
        elif self.direction == 'W':
            if int(self.x) - 2 >= 0 and self.grid[int(self.y)][int(self.x - 2)] == 'occupied':
                return
            if int(self.x) - 1 >= 0 and self.grid[int(self.y)][int(self.x - 1)] == 'occupied':
                return
            next_y += 1  # Move back up

        # Update position and mark the grid as occupied
        self.x, self.y = next_x, next_y

        if self.grid[int(self.y)][int(self.x)] != '4_way_red':
            self.grid[int(self.y)][int(self.x)] = 'occupied'

        # Reset the pulled over status
        self.pulled_over = False
        self.stopped = False

    def update_vehicle_grid_positions(self, prev_x, prev_y, current_x, current_y):
        """
        Update the grid positions of the vehicle.

        Args:
            - prev_x (int): The previous x-coordinate of the vehicle.
            - prev_y (int): The previous y-coordinate of the vehicle.
            - current_x (int): The current x-coordinate of the vehicle.
            - current_y (int): The current y-coordinate of the vehicle.

        Modifies:
            - self.grid: The grid of the city.
        """
        # Only reset the old position if the vehicle has fully left that tile and it's within the grid
        if (prev_x != current_x or prev_y != current_y) and 0 <= prev_y < GRID_SIZE and 0 <= prev_x < GRID_SIZE:
            if self.grid[prev_y][prev_x] != '4_way_red':
                self.grid[prev_y][prev_x] = 'road'

        # Set grid to occupied for the new position if it's within the grid
        if 1 <= current_y < GRID_SIZE and 1 <= current_x < GRID_SIZE:  # Changed from 0 to 1 to fix negative indexing/'occupied' bug
            if self.grid[current_y][current_x] != '4_way_red':
                self.grid[current_y][current_x] = 'occupied'

    def check_if_in_intersection(self):
        """
        Check if the vehicle is within the intersection.
        
        Returns:
            - bool: Whether the vehicle is in the intersection.
        """
        if self.direction in ['N', 'S'] and 10 <= self.y <= 13:
            return True
        elif self.direction in ['E', 'W'] and 10 <= self.x <= 13:
            return True
        return False

    def is_off_screen(self):
        """
        Check if the vehicle is off the screen.

        Returns:
            - bool: Whether the vehicle is off the screen.
        """
        return self.x < 0 or self.x > GRID_SIZE or self.y < 0 or self.y > GRID_SIZE
    


class EmergencyVehicle(Vehicle):
    """
    A class to represent an emergency vehicle in the simulation.
    
    Same attributes and methods as the Vehicle class, with the following modifications:
        - speed: The speed of the emergency vehicle is increased.
        - check_ahead: The emergency vehicle can pass through red lights.
        - flash_lights: The color of the emergency vehicle cycles between red, white, and blue.
    """
    def __init__(self, x, y, direction, city, color=(255,255,255)):
        super().__init__(x, y, direction, city, color)      # initialize the vehicle with the same attributes
        self.speed = random.uniform(0.7, 0.9) * VEHICLE_BASE_SPEED    # increase the speed of the emergency vehicle


    def check_ahead(self):
        """
        Override the check_ahead method to allow the emergency vehicle to pass through red
        """
        return False

    def flash_lights(self):
        """This function makes the color of the emergency vehicle cycle between red, white, and blue"""
        if self.color == (255, 0, 0):
            self.color = (255, 255, 255)
        elif self.color == (255, 255, 255):
            self.color = (0, 0, 255)
        else:
            self.color = (255, 0, 0)

# Vehicle Generation Functions
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

def generate_emergency_vehicle():
    """
    Generate an emergency vehicle with a random starting position, direction

    Returns:
        - tuple: The x-coordinate, y-coordinate, direction, and color of the emergency vehicle.
    """
    # Pick a random direction/starting point for the vehicle
    x, y, direction, color = generate_vehicle()

    # Set the base color of the emergency vehicle to white
    color = (255, 255, 255)

    return x, y, direction, color