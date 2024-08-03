# Import the necessary modules
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


# Main loop
grid = generate_city_grid(rows, cols)
running = True
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

    draw_grid(window, grid)  # Draw the grid on the window
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
