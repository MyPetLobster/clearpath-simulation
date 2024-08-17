# Basic Simulation Parameters
TILE_SIZE = 32              # pixels
WIDTH, HEIGHT = 768, 768    # pixels
GRID_SIZE = 24              # tiles

# Colors
BLOCK_COLOR = (0, 0, 0)
CROSSWALK_COLOR = (255, 255, 255)
ROAD_COLOR = (40, 40, 40)
SIDEWALK_COLOR = (90, 90, 90)
RED_LIGHT = (255, 0, 0)
GREEN_LIGHT = (0, 255, 0)
YELLOW_LIGHT = (255, 255, 0)
OFF_LIGHT = (108, 108, 120)
YELLOW_STRIPE = (235, 189, 52)

# Vehicle Parameters
FREQUENCY_OF_EVENTS = 0.03              # frequency of vehicle generation, 0.03 = 3% chance per frame. (~83% chance per second)
VEHICLE_BASE_SPEED = 0.2                # tiles per frame (0.2 = 12 tiles per second)        
GREEN_LIGHT_DURATION = 10               # seconds
YELLOW_LIGHT_DURATION = 3               # seconds
RED_LIGHT_DURATION = 13                 # seconds

# Analysis Parameters
ANALYSIS_PHASE_DURATION = 300

# Element References
EW_CROSSWALKS = [(10,11), (10, 12), (13, 11), (13, 12)]
NS_CROSSWALKS = [(11,10), (12,10), (11, 13), (12, 13)]
CROSSWALK_TILES = {"EW": EW_CROSSWALKS, "NS": NS_CROSSWALKS}
INTERSECTION_TILES = [(11, 11), (11, 12), (12, 11), (12, 12)]