import pygame
import sys
import random

# Initialize the pygame module
pygame.init()

# Set up display
width, height = 800, 800  # Define the width and height of the window
window = pygame.display.set_mode((width, height))  # Create the window with the specified dimensions
pygame.display.set_caption("City Grid Simulation")  # Set the title of the window

# Define some colors using RGB values
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Grid settings
rows, cols = 100, 100  # Define the number of rows and columns in the grid
cell_size = width // cols  # Calculate the size of each cell based on the window width and number of columns

# Function to generate a fake city grid
def generate_city_grid(rows, cols):
    # 'B' for buildings and 'R' for roads
    # Create a 2D list (grid) filled with 'B' for buildings, list comprehension will automatically set 'B' for each cell
    grid = [['B' for _ in range(cols)] for _ in range(rows)]

    # Create horizontal roads
    # Start from 2 and increment by 10 to leave space for buildings, range up to rows
    for i in range(2, rows, 10):
        for j in range(cols):
            grid[i][j] = 'R'  # Set the cell to 'R' for road
            grid[i+1][j] = 'R'  # Make the road two tiles wide

    # Create vertical roads
    for j in range(2, cols, 10):
        for i in range(rows):
            grid[i][j] = 'R'  # Set the cell to 'R' for road
            grid[i][j+1] = 'R'  # Make the road two tiles wide
    
    return grid  # Return the generated grid

# Function to draw the grid
def draw_grid(win, grid):
    for i in range(rows):
        for j in range(cols):
            rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)  # Create a rectangle for each cell

            # If cell is a road, draw it in gray
            if grid[i][j] == 'R':
                pygame.draw.rect(win, GRAY, rect)

            # If cell is not a road, it is a building; draw it in dark gray
            else:
                pygame.draw.rect(win, DARK_GRAY, rect)

            # Draw a white border around each cell
            pygame.draw.rect(win, WHITE, rect, 1)

# Define the TrafficLight class
class TrafficLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = random.choice(["RED", "YELLOW", "GREEN"])  # Initial random state
        self.timer = random.randint(0, 300)  # Random initial timer to prevent synchronization
        self.red_duration = 1200  # 20 seconds * 60 FPS
        self.green_duration = 1200  # 20 seconds * 60 FPS
        self.yellow_duration = 300  # 5 seconds * 60 FPS

    def update(self):
        self.timer += 1
        if self.state == "RED" and self.timer > self.red_duration:
            self.state = "GREEN"
            self.timer = 0
        elif self.state == "GREEN" and self.timer > self.green_duration:
            self.state = "YELLOW"
            self.timer = 0
        elif self.state == "YELLOW" and self.timer > self.yellow_duration:
            self.state = "RED"
            self.timer = 0

    def activate_4_way_stop(self):
        self.state = "BLINKING_RED"

    def draw(self, win):
        if self.state == "RED":
            color = RED
        elif self.state == "GREEN":
            color = GREEN
        elif self.state == "YELLOW":
            color = YELLOW
        else:
            color = WHITE  # Blinking red
        rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(win, color, rect)

# Define the Vehicle class
class Vehicle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 1
        self.path = [(i, j) for i in range(10, rows, 20) for j in range(10, cols, 20)]  # Example path

    def move(self):
        if self.path:
            next_x, next_y = self.path[0]
            if not is_light_red(next_x, next_y):
                self.x, self.y = self.path.pop(0)

    def draw(self, win):
        rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(win, self.color, rect)

# Function to check if a traffic light is red
def is_light_red(x, y):
    for light in traffic_lights:
        if light.x == x and light.y == y and light.state == "RED":
            return True
    return False

# Create traffic lights at intersections
traffic_lights = [TrafficLight(i, j) for i in range(2, rows, 10) for j in range(2, cols, 10)]

# Function to activate 4-way stop
def activate_4_way_stop(cone):
    for light in traffic_lights:
        if (light.x, light.y) in cone:
            light.activate_4_way_stop()

# Main loop
grid = generate_city_grid(rows, cols)
vehicles = [Vehicle(0, 0, GREEN)]
running = True
cone = [(10, 10), (11, 10), (10, 11), (11, 11)]  # Example cone for 4-way stop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window
            pygame.quit()
            sys.exit()

    window.fill(BLACK)  # Fill the window with a black background

    keys = pygame.key.get_pressed()  # Check which keys are pressed
    if keys[pygame.K_j]:  # If the 'j' key is pressed
        print("Stopped Manually")  # Print a debug message
        running = False  # Stop the main loop

    activate_4_way_stop(cone)  # Activate 4-way stop at specified intersections

    draw_grid(window, grid)  # Draw the grid on the window
    for light in traffic_lights:
        light.update()  # Update the traffic light state
        light.draw(window)  # Draw the traffic light
    for vehicle in vehicles:
        vehicle.move()  # Move the vehicle
        vehicle.draw(window)  # Draw the vehicle

    pygame.display.update()  # Update the display



# Scenario 1: 911 Call for a Broken Leg at a Specific Address
# Initialize map data 
# Initialize AI agents (Agent class) for event handling

# # Phase 1 - Analyze and Calculate Cone
# Function handle_911_call(caller_address, emergency_vehicle_ids): 
#     Create event object with event ID 
#     For each vehicle_id in emergency_vehicle_ids: 
#         Create vehicle object with vehicle_id 
#         Plot vehicle on map 

#     While event is active: 
#         For each vehicle in event vehicles: 
#             Update vehicle's speed, direction, x, y coordinates 
#             Calculate potential path to caller_address 
#             Define 'cone' of influence for each path

#     # Phase 2 - Action, Clear the Path, Listen
#     Function update_traffic_lights(cone): 
#         For each traffic light in cone: 
#             Set traffic light to blinking red 4-way stop 

#     Function monitor_dispatch(): 
#         Listen for keywords in dispatcher updates 
#         If transport needed to hospital: 
#             Calculate path from caller_address to hospital 
#             Extend cone to include path to hospital 
#             Update traffic lights for extended cone 
#             If dispatch overrides with specific hospital: 
#                 Recalculate path and update traffic lights 

#     While event is active: 
#         Update_traffic_lights(cone) 
#         Monitor_dispatch() 

#     End while 
# End function



# Scenario 2: Police Officer Begins to Pursue a Suspect
# Function handle_pursuit(lead_pursuer_id, supporting_vehicle_ids):
#     Create pursuit event object with event ID
#     Create lead pursuer object with lead_pursuer_id
#     Plot lead pursuer on map

#     For each vehicle_id in supporting_vehicle_ids:
#         Create vehicle object with vehicle_id
#         Plot vehicle on map

#     While pursuit is active:
#         Update lead pursuer's speed, direction, x, y coordinates
#         Calculate pursuit cone based on lead pursuer's data
#         Define wider area for pursuit cone
#     Function update_pursuit_traffic_lights(cone):
#         For each traffic light in cone:
#             Set traffic light to blinking red 4-way stop
#             Set crosswalk signals to blink "Stop" and emit audible signals

#     Function update_electronic_signs(cone):
#         For each electronic road sign in cone:
#             Display pursuit alert message

#     Function monitor_pursuit_dispatch():
#         Listen for keywords in dispatcher updates
#         If keyword detected (e.g., "gun", "erratic"):
#             Expand cone area
#             Notify schools and public venues in expanded cone
#             Update traffic lights for expanded cone

#     While pursuit is active:
#         Update_pursuit_traffic_lights(cone)
#         Update_electronic_signs(cone)
#         Monitor_pursuit_dispatch()

#     End while
#     If pursuit ends:
#         If further emergency response needed:
#             Handle as regular emergency event with ClearPath

# End function
