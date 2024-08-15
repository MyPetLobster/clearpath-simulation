import pygame as pg

from config import TILE_SIZE
from entities.vehicle import EmergencyVehicle



def draw_split_tile(window, ns_color, ew_color, x, y):
    """
    Draw a split tile with different colored triangles.
    
    Args:
        - window (Surface): The pygame window to draw on
        - ns_color (tuple): RGB color tuple for the north-south road
        - ew_color (tuple): RGB color tuple for the east-west road
        - x (int): The x-coordinate of the tile
        - y (int): The y-coordinate of the tile
        
    Returns:    
        None
    """
    # Define the corners of the selected tile that needs to be split
    top_left = (x * TILE_SIZE, y * TILE_SIZE)
    top_right = ((x + 1) * TILE_SIZE, y * TILE_SIZE)
    bottom_left = (x * TILE_SIZE, (y + 1) * TILE_SIZE)
    bottom_right = ((x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE)

    # Split tile into appropriate colored triangles
    if x == 10 and y == 10:
        pg.draw.polygon(window, ns_color, [top_left, top_right, bottom_right])
        pg.draw.polygon(window, ew_color, [top_left, bottom_left, bottom_right])
    elif x == 13 and y == 10:
        pg.draw.polygon(window, ns_color, [top_left, top_right, bottom_left])
        pg.draw.polygon(window, ew_color, [top_right, bottom_left, bottom_right])
    elif x == 13 and y == 13:
        pg.draw.polygon(window, ew_color, [top_left, top_right, bottom_right])
        pg.draw.polygon(window, ns_color, [top_left, bottom_left, bottom_right])
    elif x == 10 and y == 13:
        pg.draw.polygon(window, ew_color, [top_left, top_right, bottom_left])
        pg.draw.polygon(window, ns_color, [top_right, bottom_left, bottom_right])


def collision_counter(vehicles, collision_count, collision_pairs, collision_cooldown):
    """
    Count the total number of collisions for all vehicles in the simulation.

    Args:
        vehicles (list): List of vehicle objects.
        collision_count (int): The current collision count.
        collision_pairs (dict): A dictionary to track counted collisions.
        collision_cooldown (dict): A dictionary to track cooldowns for collisions.

    Returns:
        int: Updated collision count.
    """
    intersection_tiles = [
        (11, 11), (11, 12), (12, 11), (12, 12),
        (11, 10), (12, 10), (9, 11), (9, 12),
        (11, 13), (12, 13), (13, 11), (13, 12)
    ]

    for i, vehicle in enumerate(vehicles):
        for j, other_vehicle in enumerate(vehicles):
            if i != j:  # Ensure we don't check the same vehicle against itself
                if detect_opposing_directions(vehicle, other_vehicle):
                    if (int(vehicle.x), int(vehicle.y)) in intersection_tiles:
                        if (int(other_vehicle.x), int(other_vehicle.y)) in intersection_tiles:
                            if (isinstance(vehicle, EmergencyVehicle) or isinstance(other_vehicle, EmergencyVehicle)) and (not isinstance(vehicle, EmergencyVehicle) or not isinstance(other_vehicle, EmergencyVehicle)):
                                pair = tuple(sorted([i, j]))  # Sort to avoid (i, j) and (j, i) being treated as different
                                if pair not in collision_cooldown or collision_cooldown[pair] == 0:
                                    collision_count, detected = detect_collision(vehicle, other_vehicle, collision_pairs, collision_count, pair)
                                    if detected:
                                        collision_cooldown[pair] = 60  # Set a cooldown of 30 frames (adjust as needed)
                                else:
                                    # Decrease the cooldown for this collision pair
                                    collision_cooldown[pair] -= 1

    # Remove any pairs from the cooldown list if their cooldown has expired
    collision_cooldown = {pair: cooldown for pair, cooldown in collision_cooldown.items() if cooldown > 0}

    return collision_count


def detect_collision(vehicle, other_vehicle, collision_pairs, collision_count, pair):
    vehicle_positions = [(int(vehicle.x), int(vehicle.y))]
    other_vehicle_positions = [(int(other_vehicle.x), int(other_vehicle.y))]

    # Add previous tile positions based on direction of travel
    if vehicle.direction == 'N':
        vehicle_positions.append((int(vehicle.x) + 1, int(vehicle.y)))
    elif vehicle.direction == 'S':
        vehicle_positions.append((int(vehicle.x) - 1, int(vehicle.y) - 1))
    elif vehicle.direction == 'E':
        vehicle_positions.append((int(vehicle.x), int(vehicle.y) - 1))
    elif vehicle.direction == 'W':
        vehicle_positions.append((int(vehicle.x), int(vehicle.y) + 1))

    if vehicle.direction == 'N' or vehicle.direction == 'S':
        if other_vehicle.direction == 'E':
            other_vehicle_positions.append((int(other_vehicle.x), int(other_vehicle.y) - 1))
        elif other_vehicle.direction == 'W':
            other_vehicle_positions.append((int(other_vehicle.x), int(other_vehicle.y - 1)))
    if vehicle.direction == 'E' or vehicle.direction == 'W':
        if other_vehicle.direction == 'N':
            other_vehicle_positions.append((int(other_vehicle.x) + 1, int(other_vehicle.y)))
        elif other_vehicle.direction == 'S':
            other_vehicle_positions.append((int(other_vehicle.x) - 1, int(other_vehicle.y)))


    # Check for collisions between all combinations of positions
    for pos1 in vehicle_positions:
        for pos2 in other_vehicle_positions:
            if pos1 == pos2:
                if pair not in collision_pairs:
                    # Final check to make sure vehicles are moving in different directions
                    collision_count += 1
                    collision_pairs[pair] = True
                    return collision_count, True

    return collision_count, False

def detect_opposing_directions(vehicle, other_vehicle):
    if vehicle.direction == 'N' or vehicle.direction == 'S':
        if other_vehicle.direction == 'E' or other_vehicle.direction == 'W':
            return True
    elif vehicle.direction == 'E' or vehicle.direction == 'W':
        if other_vehicle.direction == 'N' or other_vehicle.direction == 'S':
            return True