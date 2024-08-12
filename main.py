import pygame as pg
import random
import sys

from config import *
from city import CityGrid
from entities.vehicle import Vehicle, generate_vehicle
from entities.traffic_light import TrafficLight
from helpers import draw_split_tile


# Initialize pygame
pg.init()
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ClearPath Simulation")
clock = pg.time.Clock()


class Simulation:
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

    # Add traffic lights to city grid data structure
        for light in self.traffic_lights:
            self.city.add_traffic_light(light)

    def run(self):
        # Main loop
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
        # Update traffic lights
        for light in self.traffic_lights:
            light.update()

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
            # Generate a vehicle with random starting position/direction & add it to the list
            x, y, direction, color = generate_vehicle()
            self.vehicles.append(Vehicle(x, y, direction, self.city, color))

        # Update the grid to reflect the current state of the intersection
        self.update_intersection(self.city.grid)

    def draw(self):
        self.city.draw(self.win)
        # Draw the split tiles that connect two lights
        for (x, y) in self.split_tiles:
            north_south_color = self.get_light_color(9, 10) 
            east_west_color = self.get_light_color(10,9)
            draw_split_tile(self.win, north_south_color, east_west_color, x, y)

        # Draw the traffic lights and vehicles
        for light in self.traffic_lights:
            light.draw(self.win)
        for vehicle in self.vehicles:
            vehicle.draw(self.win)


    def get_light_color(self, x, y):
        # Find the color of the light at the given position
        for light in self.traffic_lights:
            if light.x == x and light.y == y:
                if light.state == 'RED':
                    return RED_LIGHT
                elif light.state == 'YELLOW':
                    return YELLOW_LIGHT
                elif light.state == 'GREEN':
                    return GREEN_LIGHT
        return RED_LIGHT       # Fallback color, should never reach here
    
    def update_intersection(self, grid):
        for light in self.traffic_lights:
            if light.state == 'RED' or (light.state == 'YELLOW' and light.get_yellow_duration() > 1.5):
                self.mark_crosswalks_occupied(light, grid)
            else:
                self.mark_crosswalks_clear(light, grid)

    def mark_crosswalks_occupied(self, light, grid):
        crosswalks = self.get_crosswalks_for_light(light)
        for tile in crosswalks:
            grid[tile[1]][tile[0]] = 'occupied'

    def mark_crosswalks_clear(self, light, grid):
        crosswalks = self.get_crosswalks_for_light(light)
        for tile in crosswalks:
            grid[tile[1]][tile[0]] = 'crosswalk'

    def get_crosswalks_for_light(self, light):
        if light in self.ew_traffic_lights:
            return self.ew_crosswalks
        else:
            return self.ns_crosswalks
    



if __name__ == "__main__":
    sim = Simulation(WIN, clock)
    sim.run()
