import pygame as pg

from config import TILE_SIZE



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


def collision_counter(vehicles, collision_count):
    """
    Count the total number of collisions for all vehicles in the simulation.

    """
    checked_pairs = set()
    intersection_tiles = [(11, 11), (11,12), (12,11), (12,12)]

    for i, vehicle in enumerate(vehicles):
        for j, other_vehicle in enumerate(vehicles):
            if i != j:     # Ensure we don't check same vehicle against itself
                # Check for collision
                if int(vehicle.x) == int(other_vehicle.x) and int(vehicle.y) == int(other_vehicle.y):
                    pair = tuple(sorted([i, j]))  # Sort to avoid (i, j) and (j, i) being treated as different

                    # If the pair hasn't already been checked, increment the collision count
                    if pair not in checked_pairs and (int(vehicle.x), int(vehicle.y)) in intersection_tiles:
                        collision_count += 1
                        checked_pairs.add(pair)
    
    return collision_count