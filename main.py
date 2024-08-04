import pygame as pg
from sim.sim import Game


def main():

    running = True
    playing = True

    pg.init()
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menu

    # implement game
    game = Game(screen, clock)

    while running:
        # start menu goes here
    
        while playing:
            # game loop goes here
            game.run()



if __name__ == "__main__":
    main()


































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
