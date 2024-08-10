import pygame as pg
import sys
from .city import City
from .settings import TILE_SIZE


class Game: 

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        grid_len_x = self.width // TILE_SIZE
        grid_len_y = self.height // TILE_SIZE
        self.city = City(grid_len_x, grid_len_y, self.width, self.height)

    # Main Loop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)     # Set the frame rate to 60 fps
            self.events()           # Check for events
            self.update()           # Update the game
            self.draw()             # Draw the game

    # Check for events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.playing = False    # Exit the while loop
                pg.quit()               # Quit the game
                sys.exit()              # Exit the program 
            

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))    # Fill the screen with black

        for x in range(self.city.grid_len_x):
            for y in range(self.city.grid_len_y):
                square = self.city.create_city()[x][y]["cartesian_rect"]
                rect = pg.Rect(square[0][0], square[0][1], TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.screen, (255, 0, 255), rect, 1)

        pg.display.flip()              # Update the display




# https://www.youtube.com/watch?v=wI_pvfwcPgQ
