import pygame as pg
from config import TILE_SIZE, WIDTH, HEIGHT

class Scoreboard:
    """
    Class to manage the scoreboard display.
    
    Attributes:
        - big_font (Font): Font object for large text
        - font (Font): Font object for regular text
        - small_font (Font): Font object for small text
        - start_time (int): The time at which the simulation started
        - collision_count (int): The total number of collisions detected
        - clearpath_enabled (bool): Whether or not ClearPath is enabled
        - analysis_mode_active (bool): Whether or not the analysis mode is active
        
    Methods:
        - update_collision_count: Update the collision count with the latest data
        - get_time_elapsed: Get the time elapsed since the simulation started
        - draw: Draw the scoreboard on the screen
        - display_analysis_results: Display the analysis results on the screen
    """
    def __init__(self):
        self.big_font = pg.font.Font(None, 32)
        self.font = pg.font.Font(None, 24)  
        self.small_font = pg.font.Font(None, 20)
        self.tiny_font = pg.font.Font(None, 16)
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
        """
        Draw the scoreboard on the screen.
        
        Args:
            - win (Surface): The pygame window to draw on.
        """
        # Draw the background rectangle for the main scoreboard (bottom right quadrant)
        pg.draw.rect(win, (30, 30, 30), (WIDTH - 8 * TILE_SIZE, HEIGHT - 8 * TILE_SIZE, 6 * TILE_SIZE, 3.5 * TILE_SIZE), border_radius=10)

        # Render the ClearPath status text
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

        # Render the instructions text for analysis mode
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
            # Render the instructions text for base running simulation mode
            instructions_text = self.font.render("Press 'e' to toggle ERTS", True, (255, 255, 255))
            win.blit(instructions_text, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 4 * TILE_SIZE))
            instructions_text_2 = self.font.render("Press 'r' to reset sim.", True, (255, 255, 255))
            win.blit(instructions_text_2, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 3.5 * TILE_SIZE))
            instructions_text_3 = self.font.render("Press 'p' to pause sim.", True, (255, 255, 255))
            win.blit(instructions_text_3, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 3 * TILE_SIZE))
            instructions_text_4 = self.font.render("Press 'esc' to quit.", True, (255, 255, 255))
            win.blit(instructions_text_4, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 2.5 * TILE_SIZE))
            instructions_text_5 = self.font.render("Press 'a' to run 5 min analysis", True, (255, 255, 255))
            win.blit(instructions_text_5, (WIDTH - 9 * TILE_SIZE + 10, HEIGHT - 2 * TILE_SIZE))

    def display_analysis_results(self, win, analytics):
        """
        Display the analysis results on the screen.
        
        Args:
            - win (Surface): The pygame window to draw on.
            - analytics (Analytics): The analytics object containing the results to display.
        """
        # Display the analysis results on the screen (top right quadrant)
        analysis_text = self.font.render("Analysis Results", True, (255, 255, 255))
        ERTS_disabled_vehicle_count = self.small_font.render(f"ERTS Disabled: {analytics.no_erts_car_count} vehicles generated", True, (255, 0, 0))
        ERTS_disabled_emergency_count = self.small_font.render(f"ERTS Disabled: {analytics.no_erts_emergency_count} emergencies", True, (255, 0, 0))
        ERTS_disabled_collision_text = self.small_font.render(f"ERTS Disabled: {analytics.no_erts_collision_count} collisions", True, (255, 0, 0))
        ERTS_disabled_collision_rate = self.small_font.render(f"ERTS Disabled: {analytics.no_erts_collision_rate:.3f} collision rate", True, (255, 0, 0))
        ERTS_disabled_avg_weighted_collision_rate = self.small_font.render(f"ERTS Disabled: {analytics.no_erts_avg_weighted_collision_rate:.3f} avg weighted rate", True, (255, 0, 0))
        ERTS_enabled_vehicle_count = self.small_font.render(f"ERTS Enabled: {analytics.erts_car_count} vehicles generated", True, (0, 255, 0))
        ERTS_enabled_emergency_count = self.small_font.render(f"ERTS Enabled: {analytics.erts_emergency_count} emergencies", True, (0, 255, 0))
        ERTS_enabled_collision_count = self.small_font.render(f"ERTS Enabled: {analytics.erts_collision_count} collisions", True, (0, 255, 0))
        ERTS_collision_rate = self.small_font.render(f"ERTS Enabled: {analytics.erts_collision_rate:.3f} collision rate", True, (0, 255, 0))
        ERTS_base_weighted_collision_rate = self.small_font.render(f"ERTS Enabled: {analytics.erts_base_weighted_collision_rate:.3f} base weighted rate", True, (0, 255, 0))
        ERTS_avg_weighted_collision_rate = self.small_font.render(f"ERTS Enabled: {analytics.erts_avg_weighted_collision_rate:.3f} avg weighted rate", True, (0, 255, 0))
        ERTS_extrapolated_collisions = self.small_font.render(f"ERTS Enabled: {analytics.erts_extrapolated_collisions:.3f} extrapolated collisions", True, (0, 255, 0)) 
        info_text = self.tiny_font.render("* see README for info about weight calculations", True, (255, 255, 255))

        win.blit(analysis_text, (WIDTH // 2 + 5 * TILE_SIZE, TILE_SIZE * 0.3))
        win.blit(ERTS_disabled_vehicle_count, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 1.2))
        win.blit(ERTS_disabled_emergency_count, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 1.8))
        win.blit(ERTS_disabled_collision_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 2.4))
        win.blit(ERTS_disabled_collision_rate, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 3))
        win.blit(ERTS_disabled_avg_weighted_collision_rate, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 3.6))
        win.blit(ERTS_enabled_vehicle_count, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 4.6))
        win.blit(ERTS_enabled_emergency_count, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 5.2))
        win.blit(ERTS_enabled_collision_count, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 5.8))
        win.blit(ERTS_collision_rate, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 6.4))
        win.blit(ERTS_base_weighted_collision_rate, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 7))
        win.blit(ERTS_avg_weighted_collision_rate, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 7.6))
        win.blit(ERTS_extrapolated_collisions, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 8.2))
        win.blit(info_text, (WIDTH // 2 + 2.75 * TILE_SIZE, TILE_SIZE * 9.2))

        # Modify the control instructions at end of analysis (bottom right quadrant)
        instructions_text_2 = self.font.render("Press 'r' to reset sim.", True, (255, 255, 255))
        win.blit(instructions_text_2, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 5.8 * TILE_SIZE))
        instructions_text_3 = self.font.render("Press 'esc' to quit.", True, (255, 255, 255))
        win.blit(instructions_text_3, (WIDTH - 8 * TILE_SIZE + 10, HEIGHT - 5 * TILE_SIZE))


class Logo:
    """
    Class to manage the ClearPath logo display.
    
    Attributes:
        - logo (Surface): The ClearPath logo image (PNG)

    Methods:
        - draw: Draw the ClearPath logo on the screen
    """
    def __init__(self):
        self.logo = pg.image.load('assets/clearpath-logo-sign.png')
        self.logo = pg.transform.scale(self.logo, (8 * TILE_SIZE, 2.5 * TILE_SIZE))

    def draw(self, win):
        win.blit(self.logo, (1 * TILE_SIZE, 2 * TILE_SIZE))


class ERTSLogo:
    """
    Class to manage the ERTS logo display.
    
    Attributes:
        - logo_active (Surface): The ERTS logo image (active) (PNG)
        - logo_inactive (Surface): The ERTS logo image (inactive) (PNG)
        
    Methods:
        - draw: Draw the ERTS logo on the screen
    """
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
    """
    Class to manage the analysis display (while analysis mode is running).

    Attributes:
        - font (Font): Font object for regular text
        - big_font (Font): Font object for large text
        - analysis_timer (int): The time remaining in the analysis phase
        - active (bool): Whether or not the analysis phase is active
        - phase_two_active (bool): Whether or not phase two of the simulation is active
        - erts_disabled_collision_count (int): The total number of collisions detected with ERTS inactive
        - erts_enabled_collision_count (int): The total number of collisions detected with ERTS active
        - analytics (Analytics): The analytics object containing the results to display

    Methods:
        - update: Update the analysis display with the latest data
        - draw: Draw the analysis display on the screen
    """
    def __init__(self, analytics):
        self.font = pg.font.Font(None, 26)
        self.big_font = pg.font.Font(None, 32)
        self.analysis_timer = 0
        self.erts_disabled_collision_count = 0
        self.erts_enabled_collision_count = 0
        self.analytics = analytics

    def update(self, win, analysis_timer):
        """
        Update the analysis display with the latest data.
        
        Args:
            - win (Surface): The pygame window to draw on.
            
        Modifies:
            - countdown_timer (int): The time remaining in the analysis phase
            - erts_disabled_collision_count (int): The total number of collisions detected with ERTS inactive
            - erts_enabled_collision_count (int): The total number of collisions detected with ERTS active
        """
        self.erts_disabled_collision_count = self.analytics.no_erts_collision_count
        self.erts_enabled_collision_count = self.analytics.erts_collision_count
        self.analysis_timer = analysis_timer
        self.draw(win)

    def draw(self, win):
        """
        Draw the running analysis display on the screen.
        
        Args:
            - win (Surface): The pygame window to draw on.

        Modifies:
            - win (Surface): The pygame window with the analysis display drawn on it
        """
        countdown_minutes = self.analysis_timer // 60
        countdown_seconds = self.analysis_timer % 60
        analysis_text = self.big_font.render("Running Analysis...", True, (255, 255, 255))
        if countdown_minutes == 0:
            countdown_text = self.font.render(f"Time Remaining: {countdown_seconds}s", True, (255, 255, 255))
        else:
            countdown_text = self.font.render(f"Time Remaining: {countdown_minutes}m {countdown_seconds}s", True, (255, 255, 255))
        ERTS_disabled_collision_text = self.font.render(f"ERTS Disabled: {self.erts_disabled_collision_count} collisions", True, (255, 0, 0))
        ERTS_enabled_collision_text = self.font.render(f"ERTS Enabled: {self.erts_enabled_collision_count} collisions", True, (0, 255, 0))

        # Background rectangle for better visibility
        win.blit(analysis_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 3))
        win.blit(countdown_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 4))
        win.blit(ERTS_disabled_collision_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 5))
        win.blit(ERTS_enabled_collision_text, (WIDTH // 2 + 3 * TILE_SIZE, TILE_SIZE * 6))



        
