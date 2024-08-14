import pygame as pg
from config import TILE_SIZE, WIDTH, HEIGHT

class Scoreboard:
    def __init__(self):
        self.font = pg.font.Font(None, 24)  # You can change the font size if needed
        self.start_time = pg.time.get_ticks()
        self.collision_count = 0

    def update_collision_count(self, new_count):
        self.collision_count = new_count

    def get_time_elapsed(self):
        elapsed_time = pg.time.get_ticks() - self.start_time
        return elapsed_time // 1000  # Convert to seconds

    def draw(self, win):
        # Draw the background rectangle for the scoreboard
        pg.draw.rect(win, (30, 30, 30), (WIDTH - 8 * TILE_SIZE, HEIGHT - 5 * TILE_SIZE, 5 * TILE_SIZE, 3 * TILE_SIZE))

        # Render the timer text
        timer_text = self.font.render(f"Time: {self.get_time_elapsed()}s", True, (255, 255, 255))
        win.blit(timer_text, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 4.5 * TILE_SIZE))

        # Render the collision counter text
        collision_text = self.font.render(f"Collisions: {self.collision_count}", True, (255, 255, 255))
        win.blit(collision_text, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 3.5 * TILE_SIZE))

