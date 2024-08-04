import pygame as pg
import sys


class Game: 

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

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
        pg.display.flip()              # Update the display