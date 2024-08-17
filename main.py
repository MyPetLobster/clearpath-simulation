import pygame as pg
import random
import sys

from config import WIDTH, HEIGHT, GRID_SIZE, FREQUENCY_OF_EVENTS, CROSSWALK_TILES, ANALYSIS_PHASE_DURATION
from city import CityGrid
from helpers import draw_split_tile, collision_counter
from entities.scoreboard import Scoreboard, Logo, ERTSLogo, AnalysisDisplay
from entities.traffic_light import TrafficLight, IntersectionManager
from entities.vehicle import Vehicle, EmergencyVehicle, generate_vehicle, generate_emergency_vehicle


# Initialize pygame
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ClearPath Simulation")
clock = pg.time.Clock()


class Simulation:
    """
    Class to represent the simulation environment.
    
    Manages the entire simulation including vehicles, traffic lights, collisions, and analysis mode.

    Attributes:
        - win (Surface): The pygame window.
        - clock (Clock): The pygame clock.
        - city (CityGrid): The city grid object.
        - ew_traffic_lights (list): List of east-west traffic lights.
        - ns_traffic_lights (list): List of north-south traffic lights.
        - traffic_lights (list): List of all traffic lights.
        - split_tiles (list): List of split tiles that connect two lights.
        - vehicles (list): List of all vehicles in the simulation.
        - intersection_manager (IntersectionManager): The intersection manager object.
        - direction_count (dict): Dictionary to track the number of vehicles in each direction.
        - collision_count (int): The total number of collisions in the simulation.
        - collision_pairs (dict): Dictionary to track counted collisions.
        - collision_cooldown (dict): Dictionary to track cooldowns for collisions.
        - scoreboard (Scoreboard): The scoreboard object.
        - logo (Logo): The ClearPath logo object.
        - erts_logo (ERTSLogo): The ERTS logo object.
        - analysis_timer (int): Timer to track the analysis phase.
        - analysis_mode (bool): Flag to indicate if the simulation is in analysis mode.
        - analysis_results (list): List of collision counts during the analysis phase.
        - analysis_results_ready (bool): Flag to indicate if the analysis results are ready to be displayed.
        - paused (bool): Flag to indicate if the simulation is paused.

    Methods:
        - run: Main loop for the simulation.
        - update: Update the simulation state.
        - draw: Draw the simulation on the screen.
        - handle_keydown: Handle keypress events for controlling the simulation.
        - toggle_clearpath: Toggle the ClearPath mode.
        - reset_simulation: Reset the simulation to its initial state.
        - toggle_pause: Toggle the paused state of the simulation.
        - start_analysis: Start the analysis mode.
        - update_analysis: Update the analysis phase.
        - record_analysis_result: Record the current collision count during the analysis phase.
        - activate_clearpath: Activate the ClearPath system.
        - end_analysis: End the analysis phase.
        - add_vehicle: Add a vehicle to the simulation.
        - quit: Quit the simulation and close the pygame window.
    """
    def __init__(self, win, clock):
        """
        Initialize the simulation environment.
        
        Args:
            win (Surface): The pygame window.
            clock (Clock): The pygame clock.
        """
        self.win = win
        self.clock = clock
        self.city = CityGrid(GRID_SIZE)
        self.city.set_city_elements()
        self.ew_traffic_lights = [
            TrafficLight(10, 9, 'GREEN'), TrafficLight(10, 14, 'GREEN'),
            TrafficLight(13, 9, 'GREEN'), TrafficLight(13, 14, 'GREEN')
        ]
        self.ns_traffic_lights = [
            TrafficLight(9, 10), TrafficLight(14, 10),
            TrafficLight(9, 13), TrafficLight(14, 13)
        ]
        self.traffic_lights = self.ew_traffic_lights + self.ns_traffic_lights
        self.split_tiles = [(10,10), (10,13), (13,10), (13,13)]
        self.vehicles = []
        self.intersection_manager = IntersectionManager(self.city.grid, self.ew_traffic_lights, self.ns_traffic_lights)
        self.direction_count = {"N": 0, "S": 0, "E": 0, "W": 0}
        self.collision_count = 0
        self.collision_pairs = {}
        self.collision_cooldown = {}
        self.scoreboard = Scoreboard()
        self.logo = Logo()
        self.erts_logo = ERTSLogo()
        self.analysis_display = AnalysisDisplay()
        self.analysis_timer = 0
        self.analysis_mode = False
        self.analysis_results = []
        self.analysis_results_ready = False
        self.paused = False

        # Add traffic lights to city grid data structure
        for light in self.traffic_lights:
            self.city.add_traffic_light(light)

    # ---- Top Level Methods ----
    def run(self):
        """
        Main loop for the simulation.
        Handles event processing, updates, and rendering.
        """
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    self.handle_keydown(event)

            if not self.paused:
                self.update()
                self.draw()
                pg.display.flip()
                self.clock.tick(60)
        self.quit()

    def update(self):
        """
        Update the simulation state, including vehicle movements, traffic light changes, and collisions.
        """
        # Analysis Mode
        if self.analysis_mode:
            self.update_analysis()

        # Remove off-screen vehicles
        vehicles_to_remove = [vehicle for vehicle in self.vehicles if vehicle.is_off_screen()]

        # Update vehicles 
        for vehicle in self.vehicles:
            if vehicle.four_way_state == "waiting" and vehicle not in self.intersection_manager.vehicles_at_intersection:
                self.intersection_manager.vehicles_at_intersection.append(vehicle)
            vehicle.move()
            
        # Update traffic lights
        for light in self.traffic_lights:
            light.update()

        # Flash Emergency Vehicle Lights
        for vehicle in self.vehicles:
            if isinstance(vehicle, EmergencyVehicle):
                vehicle.flash_lights()

        # Have vehicles check behind for oncoming emergency vehicles
        for vehicle in self.vehicles:
            if not isinstance(vehicle, EmergencyVehicle):
                vehicle.check_behind(self.vehicles)

        # Add new vehicles
        if random.random() < FREQUENCY_OF_EVENTS:
            x, y, direction, color = generate_vehicle()
            self.add_vehicle(direction, x, y, color)

        # Add new emergency vehicles
        if random.random() < FREQUENCY_OF_EVENTS / 5:
            x, y, direction, color = generate_emergency_vehicle()
            self.vehicles.append(EmergencyVehicle(x, y, direction, self.city))

        # Check for collisions
        if len(self.vehicles) > 1:
            self.collision_count = collision_counter(self.vehicles, self.collision_count, self.collision_pairs, self.collision_cooldown)

            # Update ERTS collision counters for analysis display element
            if self.analysis_mode:
                if self.analysis_display.phase_two_active:
                    self.analysis_display.erts_enabled_collision_count = self.collision_count
                else:
                    self.analysis_display.erts_disabled_collision_count = self.collision_count

        self.scoreboard.update_collision_count(self.collision_count)

        # Provide list of emergency vehicles to the city grid (used for 4-way look_both_ways())
        emergency_vehicles = [vehicle for vehicle in self.vehicles if isinstance(vehicle, EmergencyVehicle)]
        self.city.active_emergency_vehicles = emergency_vehicles

        # Remove off-screen vehicles
        for vehicle in vehicles_to_remove:
            self.vehicles.remove(vehicle)
            if not isinstance(vehicle, EmergencyVehicle):
                self.direction_count[vehicle.direction] -= 1

        # Update the grid to reflect the current state of the intersection
        self.intersection_manager.update_intersection()

    def draw(self):
        """
        Draw the simulation on the screen, including the grid, vehicles, traffic lights, and any logos.
        """
        self.city.draw(self.win)
        # Draw the split tiles that connect two lights
        for (x, y) in self.split_tiles:
            north_south_color = self.intersection_manager.get_light_color(self.traffic_lights, 9, 10) 
            east_west_color = self.intersection_manager.get_light_color(self.traffic_lights, 10, 9)
            draw_split_tile(self.win, north_south_color, east_west_color, x, y)

        # Draw the traffic lights and vehicles
        for light in self.traffic_lights:
            light.draw(self.win)
        for vehicle in self.vehicles:
            vehicle.draw(self.win)
        
        # Draw the scoreboard or analysis results
        if self.analysis_results_ready:
            self.scoreboard.display_analysis_results(self.win, self.analysis_results)
        else:
            self.scoreboard.draw(self.win)

        # Draw main ClearPath logo top left of window
        self.logo.draw(self.win)

        # Draw ERTS logo below ClearPath logo, ACTIVE or INACTIVE
        self.erts_logo.draw(self.win, self.intersection_manager.four_way_active)
        
        if self.analysis_mode:
            self.analysis_display.draw(self.win)

    # ---- Helper Methods ----
    def handle_keydown(self, event):
        """
        Handle keypress events for controlling the simulation.
        
        Args:
            event (Event): The pygame event object.
        """
        if event.key == pg.K_ESCAPE:
            self.quit()
        elif event.key == pg.K_c:
            self.toggle_clearpath()
        elif event.key == pg.K_r:
            self.reset_simulation()
        elif event.key == pg.K_p:
            self.toggle_pause()
        elif event.key == pg.K_a:
            self.start_analysis()

    def toggle_clearpath(self):
        """
        Toggle the ClearPath mode, which activates or deactivates the 4-way red lights.
        """
        if self.intersection_manager.four_way_active:
            self.intersection_manager.deactivate_four_way_red()
            self.scoreboard.clearpath_enabled = False
        else:
            self.intersection_manager.activate_four_way_red()
            self.scoreboard.clearpath_enabled = True

    def reset_simulation(self):
        """
        Reset the simulation to its initial state.
        """
        self.__init__(self.win, self.clock)

    def toggle_pause(self):
        """
        Toggle the paused state of the simulation.
        """
        self.paused = not self.paused
        while self.paused:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.handle_keydown(event)
                if event.type == pg.QUIT:
                    self.quit()

    def start_analysis(self):
        """
        Start the analysis mode, resetting the simulation and enabling analysis.
        """
        self.reset_simulation()
        self.analysis_mode = True
        self.analysis_display.active = True
        self.analysis_display.update(self.win)

    def update_analysis(self):
        """
        Update the analysis phase by tracking collisions in both normal and ClearPath modes.
        """
        self.analysis_display.update(self.win)
        self.analysis_timer += 1
        if self.analysis_timer == ANALYSIS_PHASE_DURATION:
            self.record_analysis_result()
            self.activate_clearpath()
            self.analysis_display.phase_two_active = True
            self.analysis_display.countdown_timer = ANALYSIS_PHASE_DURATION
        elif self.analysis_timer == ANALYSIS_PHASE_DURATION * 2:
            self.record_analysis_result()
            self.end_analysis()
            self.analysis_display.active = False
            self.analysis_display.phase_two_active = False

    def record_analysis_result(self):
        """
        Record the current collision count during the analysis phase.
        """
        print(f"self.collision_count: {self.collision_count}")
        self.analysis_results.append(str(self.collision_count))
        self.collision_count = 0

    def activate_clearpath(self):
        """
        Activate the ClearPath system and reset the collision count.
        """
        self.scoreboard.clearpath_enabled = True
        self.intersection_manager.activate_four_way_red()

    def end_analysis(self):
        """
        End the analysis phase and display the results.
        """
        self.analysis_mode = False
        self.scoreboard.clearpath_enabled = False
        self.intersection_manager.deactivate_four_way_red()
        self.analysis_timer = 0
        self.collision_count = 0
        self.paused = True
        self.analysis_results_ready = True
        self.scoreboard.display_analysis_results(self.win, self.analysis_results)

    def add_vehicle(self, direction, x, y, color):
        """
        Add a vehicle to the simulation.
        
        Args:
            direction (str): The direction the vehicle is traveling.
            x (int): The x-coordinate of the vehicle.
            y (int): The y-coordinate of the vehicle.
            color (tuple): The color of the vehicle.
        """
        # Determine direction to set higher limits when light is green
        light_coords = (9, 10) if direction in ["N", "S"] else (10, 9)
        
        if self.direction_count[direction] < 12 and self.intersection_manager.get_light_color(self.traffic_lights, light_coords[0] , light_coords[1]) == (0, 255, 0):
            self.direction_count[direction] += 1
            self.vehicles.append(Vehicle(x, y, direction, self.city, color))
        elif self.direction_count[direction] < 4:
            self.direction_count[direction] += 1
            self.vehicles.append(Vehicle(x, y, direction, self.city, color))

    def quit(self):
        """
        Quit the simulation and close the pygame window.
        """
        pg.quit()
        sys.exit()




if __name__ == "__main__":
    sim = Simulation(WIN, clock)
    sim.run()
