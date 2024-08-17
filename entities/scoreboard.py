import pygame as pg
from config import TILE_SIZE, WIDTH, HEIGHT, ANALYSIS_PHASE_DURATION

class Scoreboard:
    def __init__(self):
        self.big_font = pg.font.Font(None, 32)
        self.font = pg.font.Font(None, 24)  
        self.start_time = pg.time.get_ticks()
        self.collision_count = 0
        self.clearpath_enabled = False
        self.analysis_mode_active = False

    def update_collision_count(self, new_count):
        self.collision_count = new_count

    def get_time_elapsed(self):
        elapsed_time = pg.time.get_ticks() - self.start_time
        return elapsed_time // 1000  # Convert to seconds

    def draw(self, win):
        # Draw the background rectangle for the scoreboard
        pg.draw.rect(win, (30, 30, 30), (WIDTH - 8 * TILE_SIZE, HEIGHT - 8 * TILE_SIZE, 6 * TILE_SIZE, 3.5 * TILE_SIZE), border_radius=10)


        if self.clearpath_enabled:
            clear_path_text = self.font.render("ClearPath: Enabled", True, (0, 255, 0))
            win.blit(clear_path_text, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 7.5 * TILE_SIZE))
        else:
            clear_path_text = self.font.render("ClearPath: Disabled", True, (255, 0, 0))
            win.blit(clear_path_text, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 7.5 * TILE_SIZE))


        # Render the timer text
        timer_text = self.font.render(f"Time: {self.get_time_elapsed()}s", True, (255, 255, 255))
        win.blit(timer_text, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 6.5 * TILE_SIZE))

        # Render the collision counter text
        collision_text = self.font.render(f"Collisions: {self.collision_count}", True, (255, 255, 255))
        win.blit(collision_text, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 5.5 * TILE_SIZE))

        if self.analysis_mode_active:
            instructions_text_2 = self.font.render("Press 'r' to reset sim.", True, (255, 255, 255))
            win.blit(instructions_text_2, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 3.5 * TILE_SIZE))
            instructions_text_3 = self.font.render("Press 'p' to pause analysis.", True, (255, 255, 255))
            win.blit(instructions_text_3, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 3 * TILE_SIZE))
            instructions_text_4 = self.font.render("Press 'esc' to quit.", True, (255, 255, 255))
            win.blit(instructions_text_4, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 2.5 * TILE_SIZE))
            instructions_text_5 = self.font.render("Press 'a' to restart analysis", True, (255, 255, 255))
            win.blit(instructions_text_5, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 2 * TILE_SIZE))
        else:
            instructions_text = self.font.render("Press 'c' to toggle ClearPath", True, (255, 255, 255))
            win.blit(instructions_text, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 4 * TILE_SIZE))
            instructions_text_2 = self.font.render("Press 'r' to reset sim.", True, (255, 255, 255))
            win.blit(instructions_text_2, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 3.5 * TILE_SIZE))
            instructions_text_3 = self.font.render("Press 'p' to pause sim.", True, (255, 255, 255))
            win.blit(instructions_text_3, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 3 * TILE_SIZE))
            instructions_text_4 = self.font.render("Press 'esc' to quit.", True, (255, 255, 255))
            win.blit(instructions_text_4, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 2.5 * TILE_SIZE))
            instructions_text_5 = self.font.render("Press 'a' to run 5 min analysis", True, (255, 255, 255))
            win.blit(instructions_text_5, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 2 * TILE_SIZE))

    def display_analysis_results(self, win, analysis_results):
        """ A list with two elements: [collision_count_no_clearpath, collision_count_clearpath] """
        no_clearpath_collisions = analysis_results[0]
        clearpath_collisions = analysis_results[1]

        # Draw the background rectangle for the analysis results
        # WIDTH // 2 + 3 * TILE_SIZE + 40, TILE_SIZE * 4)
        # (WIDTH - 8 * TILE_SIZE, HEIGHT - 8 * TILE_SIZE, 7 * TILE_SIZE, 3.5 * TILE_SIZE)
        pg.draw.rect(win, (30, 30, 30), (WIDTH // 2 + 3.5 * TILE_SIZE, 3 * TILE_SIZE, 8 * TILE_SIZE, 3.5 * TILE_SIZE), border_radius=10)

        # Render the analysis results
        instruction_text = self.big_font.render("Analysis Results", True, (255, 255, 255))
        win.blit(instruction_text, (WIDTH // 2 + 3.5 * TILE_SIZE + 25, 3.5 * TILE_SIZE))

        no_clearpath_text = self.font.render(f"ERTS Inactive: {no_clearpath_collisions} collisions", True, (255, 0, 0))
        win.blit(no_clearpath_text, (WIDTH // 2 + 3.5 * TILE_SIZE + 10, 4.5 * TILE_SIZE))

        clearpath_text = self.font.render(f"ERTS Active: {clearpath_collisions} collisions", True, (0, 255, 0))
        win.blit(clearpath_text, (WIDTH // 2 + 3.5 * TILE_SIZE + 10, 5.5 * TILE_SIZE))

        instructions_text_2 = self.font.render("Press 'r' to reset sim.", True, (255, 255, 255))
        win.blit(instructions_text_2, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 3 * TILE_SIZE))
        instructions_text_3 = self.font.render("Press 'esc' to quit.", True, (255, 255, 255))
        win.blit(instructions_text_3, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 2.5 * TILE_SIZE))



class Logo:
    def __init__(self):
        self.logo = pg.image.load('assets/clearpath-logo-sign.png')
        self.logo = pg.transform.scale(self.logo, (8 * TILE_SIZE, 2.5 * TILE_SIZE))

    def draw(self, win):
        win.blit(self.logo, (1 * TILE_SIZE, 2 * TILE_SIZE))


class ERTSLogo:
    def __init__(self):
        self.logo_active = pg.image.load('assets/ERTS-active.png')
        self.logo_inactive = pg.image.load('assets/ERTS-inactive.png')
        self.logo_active = pg.transform.scale(self.logo_active, (8 * TILE_SIZE, 2.5 * TILE_SIZE))
        self.logo_inactive = pg.transform.scale(self.logo_inactive, (8 * TILE_SIZE, 2.5 * TILE_SIZE))


    def draw(self, win, erts_active):
        if erts_active:
            win.blit(self.logo_active, (1 * TILE_SIZE, 5 * TILE_SIZE))
        else:
            win.blit(self.logo_inactive, (1 * TILE_SIZE, 5 * TILE_SIZE))



class AnalysisDisplay:
    def __init__(self):
        self.font = pg.font.Font(None, 26)
        self.big_font = pg.font.Font(None, 32)
        self.countdown_timer = ANALYSIS_PHASE_DURATION
        self.active = False
        self.phase_two_active = False
        self.erts_disabled_collision_count = 0
        self.erts_enabled_collision_count = 0

    def update(self, win):
        # Decrement the timer as long as the analysis phase is active and the timer has not reached zero
        print('inside analysis display update')
        print(f'self.countdown_timer: {self.countdown_timer}')
        print(f'self.active: {self.active}')
        print(f'self.phase_two_active: {self.phase_two_active}')
        if self.countdown_timer > 0 and self.active:
            self.countdown_timer -= 1
            self.draw(win)
        else:
            if self.phase_two_active:
                self.phase_two_active = False
                self.active = False
                self.countdown_timer = ANALYSIS_PHASE_DURATION


    def draw(self, win):
        countdown_seconds = self.countdown_timer // 100
        analysis_text = self.big_font.render("Running Analysis...", True, (255, 255, 255))
        countdown_text = self.font.render(f"Time Remaining: {countdown_seconds} s", True, (255, 255, 255))
        ERTS_disabled_collision_text = self.font.render(f"ERTS Disabled: {self.erts_disabled_collision_count} collisions", True, (255, 0, 0))
        ERTS_enabled_collision_text = self.font.render(f"ERTS Enabled: {self.erts_enabled_collision_count} collisions", True, (0, 255, 0))

        # Background rectangle for better visibility
        win.blit(analysis_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 3))
        win.blit(countdown_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 4))
        win.blit(ERTS_disabled_collision_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 5))
        win.blit(ERTS_enabled_collision_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 6))



        
