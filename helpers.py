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


def collision_counter(vehicles, collision_count, collision_pairs):
    """
    Count the total number of collisions for all vehicles in the simulation.

    Args:
        vehicles (list): List of vehicle objects.
        collision_count (int): The current collision count.
        collision_pairs (dict): A dictionary to track counted collisions.

    Returns:
        int: Updated collision count.
    """
    intersection_tiles = [(11, 11), (11,12), (12,11), (12,12)]

    for i, vehicle in enumerate(vehicles):
        for j, other_vehicle in enumerate(vehicles):
            if i != j:     # Ensure we don't check same vehicle against itself
                if (int(vehicle.x), int(vehicle.y)) in intersection_tiles:
                    pair = tuple(sorted([i, j]))  # Sort to avoid (i, j) and (j, i) being treated as different

                    # Check if vehicles are at the same position and this collision hasn't been counted yet
                    if int(vehicle.x) == int(other_vehicle.x) and int(vehicle.y) == int(other_vehicle.y):
                        if pair not in collision_pairs:
                            collision_count += 1
                            collision_pairs[pair] = True
                    else:
                        # If vehicles are no longer colliding, remove the pair from the dictionary
                        if pair in collision_pairs:
                            del collision_pairs[pair]

    return collision_count
