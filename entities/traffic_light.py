import pygame as pg 

from config import RED_LIGHT, YELLOW_LIGHT, GREEN_LIGHT, OFF_LIGHT, RED_LIGHT_DURATION, YELLOW_LIGHT_DURATION, GREEN_LIGHT_DURATION, TILE_SIZE, CROSSWALK_TILES


class TrafficLight:
    """
    Class to represent a traffic light

    Attributes:
        - x (int): x-coordinate of the traffic light
        - y (int): y-coordinate of the traffic light
        - state (str): Current state of the traffic light (RED, YELLOW, GREEN)
        - active_color (tuple): RGB color of the active light
        - timer (int): Timer to keep track of how long the light has been in its current state
        - yellow_timer (int): Timer to keep track of how long the light has been in the yellow state
        - blinking_red_timer (int): Timer to keep track of how long the light has been in the blinking red state

    Methods:
        - update: Update the state of the traffic light based on the timer
        - draw: Draw the traffic light on the screen
        - get_yellow_duration: Get the duration of the yellow light in seconds
    """
    def __init__(self, x, y, state='RED'):
        self.x = x
        self.y = y
        self.state = state
        self.active_color = RED_LIGHT
        self.timer = 0
        self.yellow_timer = 0
        self.blinking_red_timer = 0

    def update(self):
        """
        Update the state of the traffic light based on the timer
        
        Modifies:
            - state (str): Current state of the traffic light (RED, YELLOW, GREEN)
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

        self.active_color = color
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
        - traffic_lights (list): List of all traffic lights 
        - four_way_active (bool): Flag to indicate if the intersection is in a 4-way stop state
        - vehicles_at_intersection (list): List of vehicles currently at the intersection
        - buffer_delay (int): Delay to prevent vehicles from immediately proceeding after a 4-way stop
    
    Methods:
        - update_intersection: Update the state of the intersection based on the traffic light state
        - mark_crosswalks_occupied: Mark the crosswalks as occupied when the light is red or yellow
        - mark_crosswalks_clear: Mark the crosswalks as clear when the light is green
        - get_crosswalks_for_light: Get the crosswalks associated with a given traffic light
    """
    def __init__(self, grid, ew_traffic_lights, ns_traffic_lights):
        self.grid = grid
        self.ew_traffic_lights = ew_traffic_lights
        self.ns_traffic_lights = ns_traffic_lights
        self.traffic_lights = self.ew_traffic_lights + self.ns_traffic_lights
        self.four_way_active = False
        self.vehicles_at_intersection = []
        self.buffer_delay = 30

    def update_intersection(self):
        """
        Update the state of the intersection based on the traffic light state
        
            - Mark the crosswalks as occupied when the light is red or yellow
            - Mark the crosswalks as clear when the light is green
            
        Returns:
            None
        """
        if self.four_way_active:
            self.manage_four_way_stop()
        else:
            # Mark crosswalks as occupied or clear based on the light state 
            for light in self.traffic_lights:
                # Yellow light is considered red if it's been active for more than 0.8 seconds
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
            return CROSSWALK_TILES['EW']
        else:
            return CROSSWALK_TILES['NS']

    def get_light_color(self, traffic_lights, x, y):
        """
        Get the color of the light at a given position

        Args:
            - traffic_lights (list): List of traffic lights
            - x (int): x-coordinate of the light
            - y (int): y-coordinate of the light

        Returns:
            - color (tuple): RGB color of the light
        """
        state_colors = {
            'RED': RED_LIGHT,
            'YELLOW': YELLOW_LIGHT,
            'GREEN': GREEN_LIGHT
        }

        for light in traffic_lights:
            if light.x == x and light.y == y:
                if light.state == '4_WAY_RED':
                    return light.active_color
                return state_colors.get(light.state, RED_LIGHT)
        
        return RED_LIGHT  # Fallback color, should never reach here
    
    def activate_four_way_red(self):
        """
        Turn all traffic lights to blinking red.

        Modifies:
            - traffic_lights: Set all traffic lights to '4_WAY_RED' state
            - grid: Mark all crosswalk tiles as '4_way
        """
        for light in self.traffic_lights:
            light.state = '4_WAY_RED'
            light.timer = 0
            light.yellow_timer = 0

        crosswalks = CROSSWALK_TILES['EW'] + CROSSWALK_TILES['NS']
        for tile in crosswalks:
            # Mark all crosswalk tiles as '4_way_stop'
            self.grid[tile[0]][tile[1]] = '4_way_red'

        self.four_way_active = True
        self.update_intersection()

    def deactivate_four_way_red(self):
        """
        Resume normal traffic light operation.

        Modifies:
            - traffic_lights: Reset all traffic lights to their original state
        """
        self.four_way_active = False

        # Reset all traffic lights to their original state
        for light in self.ew_traffic_lights:
            light.state = 'RED'
            light.timer = 0
            light.yellow_timer = 0
        for light in self.ns_traffic_lights:
            light.state = 'GREEN'
            light.timer = 0
            light.yellow_timer = 0

        self.update_intersection()

    def manage_four_way_stop(self):
        """
        Manage the 4-way stop state of the intersection
        
        - Vehicles must wait for all other vehicles to clear the intersection before proceeding
        
        Modifies:
            - vehicles_at_intersection: Remove vehicles that have cleared the intersection
            - buffer_delay: Delay to prevent vehicles from immediately proceeding after a 4-way stop
        """
        self.buffer_delay = max(0, self.buffer_delay - 1)
        self.vehicles_at_intersection = [v for v in self.vehicles_at_intersection if v.four_way_state == "waiting"]
        if self.vehicles_at_intersection:
            # Determine which vehicle has been waiting the longest
            first_vehicle = max(self.vehicles_at_intersection, key=lambda v: v.four_way_timer)
            if first_vehicle.four_way_timer >= 120 and self.buffer_delay == 0:
                if first_vehicle.look_both_ways():
                    first_vehicle.four_way_state = "proceeding"
                    self.buffer_delay = 90
                else:
                    first_vehicle.four_way_state = "waiting"