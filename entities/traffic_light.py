import pygame as pg 

from config import RED_LIGHT, YELLOW_LIGHT, GREEN_LIGHT, RED_LIGHT_DURATION, YELLOW_LIGHT_DURATION, GREEN_LIGHT_DURATION, TILE_SIZE


class TrafficLight:
    def __init__(self, x, y, state='RED'):
        self.x = x
        self.y = y
        self.state = state
        self.timer = 0
        self.yellow_timer = 0

    def update(self):
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

    def draw(self, win):
        # Draw the light
        if self.state == 'RED':
            color = RED_LIGHT
        elif self.state == 'YELLOW':
            color = YELLOW_LIGHT
        else:
            color = GREEN_LIGHT

        pg.draw.rect(win, color, (self.y * TILE_SIZE, self.x * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def get_yellow_duration(self):
        return self.yellow_timer / 60  # Convert frames to seconds


class IntersectionManager:
    def __init__(self, grid, ew_traffic_lights, ns_traffic_lights, ew_crosswalks, ns_crosswalks):
        self.grid = grid
        self.ew_traffic_lights = ew_traffic_lights
        self.ns_traffic_lights = ns_traffic_lights
        self.traffic_lights = self.ew_traffic_lights + self.ns_traffic_lights
        self.ew_crosswalks = ew_crosswalks
        self.ns_crosswalks = ns_crosswalks

    def update_intersection(self):
        for light in self.traffic_lights:
            if light.state == 'RED' or (light.state == 'YELLOW' and light.get_yellow_duration() > 1.5):
                self.mark_crosswalks_occupied(light)
            else:
                self.mark_crosswalks_clear(light)

    def mark_crosswalks_occupied(self, light):
        crosswalks = self.get_crosswalks_for_light(light)
        for tile in crosswalks:
            self.grid[tile[1]][tile[0]] = 'occupied'

    def mark_crosswalks_clear(self, light):
        crosswalks = self.get_crosswalks_for_light(light)
        for tile in crosswalks:
            self.grid[tile[1]][tile[0]] = 'crosswalk'

    def get_crosswalks_for_light(self, light):
        if light in self.ew_traffic_lights:
            return self.ew_crosswalks
        else:
            return self.ns_crosswalks


def get_light_color(traffic_lights, x, y):
    # Find the color of the light at the given position
    for light in traffic_lights:
        if light.x == x and light.y == y:
            if light.state == 'RED':
                return RED_LIGHT
            elif light.state == 'YELLOW':
                return YELLOW_LIGHT
            elif light.state == 'GREEN':
                return GREEN_LIGHT
    return RED_LIGHT       # Fallback color, should never reach here