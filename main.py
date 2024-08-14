import pygame as pg
import random
import sys

from config import WIDTH, HEIGHT, GRID_SIZE, FREQUENCY_OF_EVENTS
from city import CityGrid
from entities.vehicle import Vehicle, EmergencyVehicle, generate_vehicle, generate_emergency_vehicle
from entities.traffic_light import TrafficLight, IntersectionManager, get_light_color
from entities.scoreboard import Scoreboard
from helpers import draw_split_tile, collision_counter





# Initialize pygame
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ClearPath Simulation")
clock = pg.time.Clock()


class Simulation:
    """
    Class to represent the simulation environment
    
    Attributes:
        - win (Surface): The pygame window
        - clock (Clock): The pygame clock
        - city (CityGrid): The city grid
        - ew_traffic_lights (list): List of east-west traffic lights
        - ns_traffic_lights (list): List of north-south traffic lights
        - traffic_lights (list): List of all traffic lights
        - ew_crosswalks (list): List of east-west crosswalks
        - ns_crosswalks (list): List of north-south crosswalks
        - split_tiles (list): List of split tiles
        - vehicles (list): List of vehicles in the simulation
        - intersection_manager (IntersectionManager): The intersection manager

    Methods:
        - run: Main loop for the simulation
        - update: Update the simulation state
        - draw: Draw the simulation on the screen
    """
    def __init__(self, win, clock):
        self.win = win
        self.clock = clock
        self.city = CityGrid(GRID_SIZE)
        self.city.set_city_elements()
        self.ew_traffic_lights = [TrafficLight(10, 9, 'GREEN'), TrafficLight(10, 14, 'GREEN'), TrafficLight(13, 9, 'GREEN'), TrafficLight(13, 14, 'GREEN')]
        self.ns_traffic_lights = [TrafficLight(9, 10), TrafficLight(14, 10), TrafficLight(9, 13), TrafficLight(14, 13)]
        self.traffic_lights = self.ew_traffic_lights + self.ns_traffic_lights
        self.ew_crosswalks = [(10,11), (10, 12), (13, 11), (13, 12)]
        self.ns_crosswalks = [(11,10), (12,10), (11, 13), (12, 13)]
        self.split_tiles = [(10,10), (10,13), (13,10), (13,13)]
        self.vehicles = []
        self.intersection_manager = IntersectionManager(self.city.grid, self.ew_traffic_lights, self.ns_traffic_lights, self.ew_crosswalks, self.ns_crosswalks)
        self.direction_count = {"N": 0, "S": 0, "E": 0, "W": 0}
        self.collision_count = 0
        self.collision_pairs = {}
        self.scoreboard = Scoreboard()


        # Add traffic lights to city grid data structure
        for light in self.traffic_lights:
            self.city.add_traffic_light(light)

    def run(self):
        """
        Main loop for the simulation
        
        Returns:
            None
        """
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE or event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    sys.exit()

            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(60)
        pg.quit()
        sys.exit()

    def update(self):
        """
        Update the simulation state

        Returns:
            None
        """
        # Update vehicles
        vehicles_to_remove = []
        for vehicle in self.vehicles:
            vehicle.move()
            if vehicle.is_off_screen():
                vehicles_to_remove.append(vehicle)
                
        # Update traffic lights
        for light in self.traffic_lights:
            light.update()

        # Flash Emergency Vehicle Lights
        for vehicle in self.vehicles:
            if isinstance(vehicle, EmergencyVehicle):
                if vehicle.code3:
                    vehicle.flash_lights()

        # Have vehicles check behind for oncoming emergency vehicles
        for vehicle in self.vehicles:
            if isinstance(vehicle, EmergencyVehicle) and vehicle.code3:
                pass
            else:
                vehicle.check_behind(self.vehicles)

        # Remove off-screen vehicles
        for vehicle in vehicles_to_remove:
            self.vehicles.remove(vehicle)
            self.direction_count[vehicle.direction] -= 1

        # Add new vehicles
        if random.random() < FREQUENCY_OF_EVENTS:
            # Generate a vehicle with random starting position/direction & add it to the list
            x, y, direction, color = generate_vehicle()
            if self.direction_count[direction] < 4:
                self.direction_count[direction] += 1
                self.vehicles.append(Vehicle(x, y, direction, self.city, color))

        # Add new emergency vehicles
        if random.random() < FREQUENCY_OF_EVENTS / 4:
            # Generate an emergency vehicle with random starting position/direction & add it to the list
            x, y, direction, is_code3 = generate_emergency_vehicle()
            if self.direction_count[direction] < 6:
                self.direction_count[direction] += 1
                self.vehicles.append(EmergencyVehicle(x, y, direction, self.city, is_code3))

        # Check for collisions
        if len(self.vehicles) > 1:
            self.collision_count = collision_counter(self.vehicles, self.collision_count, self.collision_pairs)

        self.scoreboard.update_collision_count(self.collision_count)

        # Update the grid to reflect the current state of the intersection
        self.intersection_manager.update_intersection()

    def draw(self):
        """
        Draw the simulation on the screen
        
        Returns:
            None
        """
        self.city.draw(self.win)
        # Draw the split tiles that connect two lights
        for (x, y) in self.split_tiles:
            north_south_color = get_light_color(self.traffic_lights, 9, 10) 
            east_west_color = get_light_color(self.traffic_lights, 10,9)

            # Draw, color the split traffic light tiles
            draw_split_tile(self.win, north_south_color, east_west_color, x, y)

        # Draw the traffic lights and vehicles
        for light in self.traffic_lights:
            light.draw(self.win)
        for vehicle in self.vehicles:
            vehicle.draw(self.win)

        self.scoreboard.draw(self.win)

    


if __name__ == "__main__":
    sim = Simulation(WIN, clock)
    sim.run()
