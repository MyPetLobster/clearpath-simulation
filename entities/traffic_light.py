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