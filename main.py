import pygame as pg
import sys



# Initialize pygame
pg.init()

# Set up display
WIDTH, HEIGHT = 800, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("ClearPath Simulation")

# Set up colors
ROAD_COLOR = (40, 40, 40)
SIDEWALK_COLOR = (90, 90, 90)
RED_LIGHT = (255, 0, 0)
GREEN_LIGHT = (0, 255, 0)
YELLOW_LIGHT = (255, 255, 0)
YELLOW_STRIPE = (225, 225, 15)
BLOCK_COLOR = (0, 0, 0)




# Function to generate city grid
def create_grid():
    grid = []
    for i in range(24):
        grid.append([])
        for j in range(24):
            grid[i].append(0)
    return grid


def set_city_elements(grid):
    # Set up roads
    for i in range(24):
        grid[11][i] = 1
        grid[i][11] = 1
        grid[12][i] = 1
        grid[i][12] = 1

    # Set up sidewalks
    for i in range(24):
        grid[10][i] = 2
        grid[i][10] = 2
        grid[13][i] = 2
        grid[i][13] = 2

def set_traffic_lights(grid):
    # Set up traffic lights
    east_west_lights = [[10][9], [10][14], [13][9], [13][14]]
    north_south_lights = [[9][10], [14][10], [9][13], [14][13]]
    cells_to_split = [[10][10], [10][13], [13][10], [13][13]]

    for cell in east_west_lights:
        grid[cell[0]][cell[1]] = 3
    for cell in north_south_lights:
        grid[cell[0]][cell[1]] = 4
    for cell in cells_to_split:
        grid[cell[0]][cell[1]] = 5







def draw_split_cell(cell):
    # Split cell into two triangles
    pass



# function to paint grid as road with intersection, and sidewalks and lights




# Class for traffic light objects (include cell location, color, and state)
# TODO: How to split one cell into triangle for cell where two traffic lights meet?
# Traffic light needs timer and rules


# Class for pedestrians (include cell location, speed, direction, and state)


# Class for vehicles


# Class for emergency vehicles


# Class for events (911 call, pursuit, etc.)


# Rules for intersection, include what cells cars should stop at, what cells pedestrians should stop at, etc.
## If traffic light turns yellow, cars should stop at intersection unless < 2 seconds of yellow have passed and 
## they are in the nearest cell to the intersection
## If traffic light turns red, cars should stop at intersection or behind the stopped car in front of them

# If 4-way stop is in effect, cars should stop and 'check' if other cars are stopped before proceeding
# TODO: write 4-way stop algorithm


# 
































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
