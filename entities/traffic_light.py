import pygame as pg 

from config import RED_LIGHT, YELLOW_LIGHT, GREEN_LIGHT, OFF_LIGHT, RED_LIGHT_DURATION, YELLOW_LIGHT_DURATION, GREEN_LIGHT_DURATION, TILE_SIZE


class TrafficLight:
    """
    Class to represent a traffic light

    Attributes:
        - x (int): x-coordinate of the traffic light
        - y (int): y-coordinate of the traffic light
        - state (str): Current state of the traffic light (RED, YELLOW, GREEN)
        - timer (int): Timer to keep track of how long the light has been in its current state
        - yellow_timer (int): Timer to keep track of how long the light has been in the yellow state

    Methods:
        - update: Update the state of the traffic light based on the timer
        - draw: Draw the traffic light on the screen
        - get_yellow_duration: Get the duration of the yellow light in seconds
    """
    def __init__(self, x, y, state='RED'):
        self.x = x
        self.y = y
        self.state = state
        self.timer = 0
        self.yellow_timer = 0
        self.blinking_red_timer = 0

    def update(self):
        """
        Update the state of the traffic light based on the timer
        
            - The traffic light will cycle through the following states:
                RED -> YELLOW -> GREEN -> RED
            - The duration of each state is defined in the config file

        Returns:
            None
        """
        self.timer += 1
        if self.state == 'YELLOW':
            self.yellow_timer += 1
        else:
            self.yellow_timer = 0

        if self.state == 'GREEN' and self.timer >= GREEN_LIGHT_DURATION * 60:
            self.state = 'YELLOW'
            self.timer = 0
        elif self.state == 'YELLOW' and self.timer >= YELLOW_LIGHT_DURATION * 60:
            self.state = 'RED'
            self.timer = 0
        elif self.state == 'RED' and self.timer >= RED_LIGHT_DURATION * 60:
            self.state = 'GREEN'
            self.timer = 0
        elif self.state == '4_WAY_RED':
            self.blinking_red_timer += 1
            self.timer = 0

    def draw(self, win):
        """
        Draw the traffic light on the screen

        Args:
            - win (pygame.Surface): The window to draw the traffic light on
        """
        if self.state == 'RED':
            color = RED_LIGHT
        elif self.state == 'YELLOW':
            color = YELLOW_LIGHT
        elif self.state == 'GREEN':
            color = GREEN_LIGHT
        elif self.state == '4_WAY_RED':
            if (self.x, self.y) in [(9, 10), (9, 13), (14, 10), (14, 13)]:
                color = RED_LIGHT
            else:
                color = OFF_LIGHT

            # Alternate between red and off every 0.5 seconds
            if self.blinking_red_timer % 30 < 15:
                if color == RED_LIGHT:
                    color = OFF_LIGHT
                else:
                    color = RED_LIGHT
            
        pg.draw.rect(win, color, (self.y * TILE_SIZE, self.x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def get_yellow_duration(self):
        """
        Returns:
            - float: Duration of the yellow light in seconds
        """
        return self.yellow_timer / 60


class IntersectionManager:
    """
    Class to manage the state of the intersection
    
    Attributes:
        - grid (list): 2D list representing the city grid
        - ew_traffic_lights (list): List of traffic lights on the east-west road
        - ns_traffic_lights (list): List of traffic lights on the north-south road
        - ew_crosswalks (list): List of crosswalks on the east-west road
        - ns_crosswalks (list): List of crosswalks on the north-south road
    
    Methods:
        - update_intersection: Update the state of the intersection based on the traffic light state
        - mark_crosswalks_occupied: Mark the crosswalks as occupied when the light is red or yellow
        - mark_crosswalks_clear: Mark the crosswalks as clear when the light is green
        - get_crosswalks_for_light: Get the crosswalks associated with a given traffic light
    """
    def __init__(self, grid, ew_traffic_lights, ns_traffic_lights, ew_crosswalks, ns_crosswalks):
        self.grid = grid
        self.ew_traffic_lights = ew_traffic_lights
        self.ns_traffic_lights = ns_traffic_lights
        self.traffic_lights = self.ew_traffic_lights + self.ns_traffic_lights
        self.ew_crosswalks = ew_crosswalks
        self.ns_crosswalks = ns_crosswalks
        self.four_way_active = False

    def update_intersection(self):
        """
        Update the state of the intersection based on the traffic light state
        
            - Mark the crosswalks as occupied when the light is red or yellow
            - Mark the crosswalks as clear when the light is green
            
        Returns:
            None
        """
        if self.four_way_active:
            return
        
        for light in self.traffic_lights:
            if light.state == 'RED' or (light.state == 'YELLOW' and light.get_yellow_duration() > 0.8):
                self.mark_crosswalks_occupied(light)
            else:
                self.mark_crosswalks_clear(light)

    def mark_crosswalks_occupied(self, light):
        """
        Mark the crosswalks as occupied when the light is red or yellow
        
        Args:
            - light (TrafficLight): The traffic light to check
            
        Returns:   
            None
        """
        crosswalks = self.get_crosswalks_for_light(light)
        for tile in crosswalks:
            self.grid[tile[1]][tile[0]] = 'red_light'

    def mark_crosswalks_clear(self, light):
        """
        Mark the crosswalks as clear when the light is green

        Args:
            - light (TrafficLight): The traffic light to check

        Returns:
            None
        """
        crosswalks = self.get_crosswalks_for_light(light)
        for tile in crosswalks:
            self.grid[tile[1]][tile[0]] = 'green_light'

    def get_crosswalks_for_light(self, light):
        """
        Get the crosswalks associated with a given traffic light

        Args:
            - light (TrafficLight): The traffic light to check

        Returns:
            - list: List of crosswalks associated with the traffic light
        """
        if light in self.ew_traffic_lights:
            return self.ew_crosswalks
        else:
            return self.ns_crosswalks

    def get_light_color(self,traffic_lights, x, y):
        """
        Get the color of the light at a given position

        Args:
            - traffic_lights (list): List of traffic lights
            - x (int): x-coordinate of the light
            - y (int): y-coordinate of the light

        Returns:
            - color (tuple): RGB color of the light
        """
        for light in traffic_lights:
            if light.x == x and light.y == y:
                if light.state == 'RED':
                    return RED_LIGHT
                elif light.state == 'YELLOW':
                    return YELLOW_LIGHT
                elif light.state == 'GREEN':
                    return GREEN_LIGHT
        return RED_LIGHT       # Fallback color, should never reach here
    
    def activate_four_way_red(self):
        """
        Turn all traffic lights to blinking red.
        """
        for light in self.traffic_lights:
            light.state = '4_WAY_RED'
            light.timer = 0
            light.yellow_timer = 0

        crosswalks = self.ew_crosswalks + self.ns_crosswalks
        for tile in crosswalks:
            # Mark all above crosswalk tiles as '4_way_stop'
            self.grid[tile[0]][tile[1]] = '4_way_red'

        self.four_way_active = True
        self.update_intersection()

        return True

    def determine_first_car(vehicles):
        """
        Determine the first car in the intersection

        Args:
            - vehicles (list): List of vehicle objects

        Returns:
            - Vehicle: The first vehicle in the intersection
        """
        first_car = None
        vehicles_at_light = {}
        for vehicle in vehicles:
            vehicles_at_light[vehicle.four_way_timer] = vehicle

        if vehicles_at_light:
            # Find out which car has been waiting the longest by sorting the dictionary keys (timer values)
            first_car = vehicles_at_light[max(vehicles_at_light.keys())]

        return first_car