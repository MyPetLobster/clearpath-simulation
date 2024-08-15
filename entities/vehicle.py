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
        # Check if the vehicle should pull over for an emergency vehicle
        if self.pulled_over:
            return

        # Check if the vehicle should stop at a 4-way stop
        if self.four_way_state == "waiting":
            self.wait_time += 1
            if self.wait_time >= 60:  # Wait for 1 second (60 frames)
                self.four_way_state = "proceeding"
                self.wait_time = 0
            return
        elif self.four_way_state == "proceeding":
            if not self.in_intersection:
                self.four_way_state = "approaching"

        if self.check_ahead():
            self.stopped = True
            return
        else:
            self.stopped = False

        

        # Check ahead to decide if the vehicle should stop
        if self.check_ahead():
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
            if self.grid[prev_y][prev_x] != '4_way_red':
                self.grid[prev_y][prev_x] = 'road'

        # Set grid to occupied for the new position if it's within the grid
        if 1 <= current_y < GRID_SIZE and 1 <= current_x < GRID_SIZE:  # Changed from 0 to 1 to fix negative indexing/'occupied' bug
            if self.grid[current_y][current_x] != '4_way_red':
                self.grid[current_y][current_x] = 'occupied'

        # Check if vehicle has entered or exited the intersection
        if self.direction in ['N', 'S'] and 10 <= self.y <= 13:
            self.in_intersection = True
        elif self.direction in ['E', 'W'] and 10 <= self.x <= 13:
            self.in_intersection = True
        else:
            self.in_intersection = False



    def check_ahead(self):
        """
        Check if the vehicle should stop based on the traffic light ahead and the next tile.
        
        Args:
            None
            
        Returns:
            - bool: Whether the vehicle should stop.
        """

        print(f'vehicle.four_way_state = {self.four_way_state}')
        # Check if in an intersection, if so continue through
        if self.in_intersection:
            return False
        
        # TODO - Figure out how to just use a loop here DRY
        # Check if the tile 2 units ahead is occupied
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
            if self.grid[next_y][next_x] == 'occupied' or self.grid[next_y][next_x] == 'red_light':
                return True

            if self.grid[next_y][next_x] == '4_way_red':
                if self.four_way_state == "approaching":
                    self.four_way_state = "waiting"
                    self.four_way_timer += 1
                if self.four_way_state == "proceeding":
                    return False
            
            
            
        # Check if the tile 1 unit ahead is occupied
        if self.direction == 'N':
            next_y = int(self.y - 1)
        elif self.direction == 'S':
            next_y = int(self.y + 1)
        elif self.direction == 'E':
            next_x = int(self.x + 1)
        elif self.direction == 'W':
            next_x = int(self.x - 1)

        # Ensure next_x and next_y are within bounds before accessing the grid
        if 0 <= next_y < GRID_SIZE and 0 <= next_x < GRID_SIZE:
            # If the next tile is occupied, stop the vehicle
            if self.grid[next_y][next_x] == 'occupied' or self.grid[next_y][next_x] == '4_way_red' or self.grid[next_y][next_x] == 'red_light':
                return True
            
        # If we've reached this point, there's no reason to stop
        return False
    
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
            # Check if it's safe to merge back
            self.merge(vehicles)
        else:
            # Check the area behind and ahead for Code 3 emergency vehicles
            for vehicle in vehicles:
                if isinstance(vehicle, EmergencyVehicle) and vehicle.code3:
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
            if self.direction == "N" and self.y - 2 <= vehicle.y <= self.y + 5:
                return True
            elif self.direction == "S" and self.y - 5 <= vehicle.y <= self.y + 2:
                return True
            elif self.direction == "E" and self.x - 5 <= vehicle.x <= self.x + 2:
                return True
            elif self.direction == "W" and self.x - 2 <= vehicle.x <= self.x + 5:
                return True
        return False
    
    def pull_over(self):
        """
        Move the vehicle to the right side of the road if there's an emergency vehicle approaching.
        """
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
        """
        # Check if there's still an emergency vehicle within the danger zone
        for vehicle in vehicles:
            if isinstance(vehicle, EmergencyVehicle) and vehicle.code3:
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
        self.code3 = code3    # whether the vehicle is in code 3 mode (lights and sirens)
        if self.code3:
            self.speed = VEHICLE_BASE_SPEED * 0.7    # increase the speed of the emergency vehicle
        else:
            self.speed = VEHICLE_BASE_SPEED

    def check_ahead(self):
        """
        Check if the vehicle should stop based on the traffic light ahead and the next tile.
        ** Emergency vehicles will ignore traffic lights if running code 3. **

        Args:
            None

        Returns:
            - bool: Whether the vehicle should stop.
        """
        if self.code3:
            return False
        else:
            return super().check_ahead()

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

    # is_code3 = random.random() < 0.8       # 50% chance of generating a vehicle in code 3 mode
    is_code3 = True

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