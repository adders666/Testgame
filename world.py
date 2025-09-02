import random
import pickle
import os

COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
]

class World:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.blocks = {} # Using a dictionary for sparse storage

    def set_block(self, x, y, z, color):
        self.blocks[(x, y, z)] = color

    def get_block(self, x, y, z):
        return self.blocks.get((x, y, z))

def generate_world(width, depth, max_height):
    world = World(width, max_height, depth)
    for x in range(width):
        for z in range(depth):
            height = random.randint(1, max_height)
            for y in range(height):
                color = random.choice(COLORS)
                world.set_block(x, y, z, color)
    return world

def save_world(world, filename):
    if not os.path.exists('worlds'):
        os.makedirs('worlds')
    filepath = os.path.join('worlds', filename)
    with open(filepath, 'wb') as f:
        pickle.dump(world, f)
    print(f"World saved to {filepath}")

def load_world(filename):
    filepath = os.path.join('worlds', filename)
    if not os.path.exists(filepath):
        print(f"Error: Save file not found at {filepath}")
        return None
    with open(filepath, 'rb') as f:
        world = pickle.load(f)
    print(f"World loaded from {filepath}")
    return world
