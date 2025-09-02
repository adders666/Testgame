import pygame
import sys
from world import generate_world, save_world, load_world
import os

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
SKY_BLUE = (135, 206, 235)

TILE_WIDTH = 32
TILE_HEIGHT = 16
BLOCK_HEIGHT = 16

def to_iso(x, y, z, camera_offset):
    iso_x = (x - z) * TILE_WIDTH / 2
    iso_y = (x + z) * TILE_HEIGHT / 2 - y * BLOCK_HEIGHT
    return iso_x + camera_offset[0], iso_y + camera_offset[1]

def draw_cube(surface, sx, sy, color):
    darken_factor1 = 0.7
    darken_factor2 = 0.5
    left_color = tuple(c * darken_factor1 for c in color)
    right_color = tuple(c * darken_factor2 for c in color)

    top_points = [
        (sx, sy),
        (sx - TILE_WIDTH / 2, sy + TILE_HEIGHT / 2),
        (sx, sy + TILE_HEIGHT),
        (sx + TILE_WIDTH / 2, sy + TILE_HEIGHT / 2)
    ]
    pygame.draw.polygon(surface, color, top_points)
    pygame.draw.polygon(surface, BLACK, top_points, 1)

    left_points = [
        (sx - TILE_WIDTH / 2, sy + TILE_HEIGHT / 2),
        (sx, sy + TILE_HEIGHT),
        (sx, sy + TILE_HEIGHT + BLOCK_HEIGHT),
        (sx - TILE_WIDTH / 2, sy + TILE_HEIGHT / 2 + BLOCK_HEIGHT)
    ]
    pygame.draw.polygon(surface, left_color, left_points)
    pygame.draw.polygon(surface, BLACK, left_points, 1)

    right_points = [
        (sx + TILE_WIDTH / 2, sy + TILE_HEIGHT / 2),
        (sx, sy + TILE_HEIGHT),
        (sx, sy + TILE_HEIGHT + BLOCK_HEIGHT),
        (sx + TILE_WIDTH / 2, sy + TILE_HEIGHT / 2 + BLOCK_HEIGHT)
    ]
    pygame.draw.polygon(surface, right_color, right_points)
    pygame.draw.polygon(surface, BLACK, right_points, 1)

def game_screen(screen, world):
    camera_offset = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4]
    font = pygame.font.Font(None, 30)
    save_button = pygame.Rect(10, 10, 100, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if save_button.collidepoint(event.pos):
                    filename = input("Enter filename to save world (e.g., my_world.dat): ")
                    if filename:
                        save_world(world, filename)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill(SKY_BLUE)
        if world and world.blocks:
            sorted_blocks = sorted(world.blocks.items(), key=lambda item: (item[0][0] + item[0][2], item[0][1]))
            for (x, y, z), color in sorted_blocks:
                sx, sy = to_iso(x, y, z, camera_offset)
                if sx > SCREEN_WIDTH + TILE_WIDTH or sx < -TILE_WIDTH or sy > SCREEN_HEIGHT + TILE_HEIGHT or sy < -BLOCK_HEIGHT * world.height:
                    continue
                draw_cube(screen, sx, sy, color)
        pygame.draw.rect(screen, GRAY, save_button)
        save_text = font.render("Save", True, BLACK)
        screen.blit(save_text, (save_button.x + 30, save_button.y + 10))
        pygame.display.flip()

def new_world_screen(screen):
    print("Generating new world...")
    world = generate_world(16, 16, 8)
    print(f"World generated with {len(world.blocks)} blocks!")
    game_screen(screen, world)

def load_world_menu(screen):
    print("Load world menu...")
    font = pygame.font.Font(None, 40)
    try:
        saved_worlds = [f for f in os.listdir('worlds') if os.path.isfile(os.path.join('worlds', f))]
    except FileNotFoundError:
        saved_worlds = []
    buttons = []
    for i, world_name in enumerate(saved_worlds):
        button = pygame.Rect(250, 100 + i * 60, 300, 50)
        buttons.append((button, world_name))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, world_name in buttons:
                    if button.collidepoint(event.pos):
                        print(f"Loading {world_name}...")
                        world = load_world(world_name)
                        if world:
                            game_screen(screen, world)
                        running = False
        screen.fill(BLACK)
        title_text = font.render("Select a World to Load", True, WHITE)
        screen.blit(title_text, (200, 30))
        if not buttons:
            no_saves_text = font.render("No saved worlds found.", True, WHITE)
            screen.blit(no_saves_text, (220, 250))
        else:
            for button, world_name in buttons:
                pygame.draw.rect(screen, GRAY, button)
                text = font.render(world_name, True, BLACK)
                screen.blit(text, (button.x + 20, button.y + 10))
        esc_text = pygame.font.Font(None, 30).render("Press ESC to go back", True, WHITE)
        screen.blit(esc_text, (10, SCREEN_HEIGHT - 40))
        pygame.display.flip()

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Block World - Main Menu")
    font = pygame.font.Font(None, 50)
    new_world_button = pygame.Rect(300, 200, 200, 50)
    load_world_button = pygame.Rect(300, 300, 200, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_world_button.collidepoint(event.pos):
                    new_world_screen(screen)
                if load_world_button.collidepoint(event.pos):
                    load_world_menu(screen)
        screen.fill(BLACK)
        pygame.draw.rect(screen, GRAY, new_world_button)
        new_world_text = font.render("New World", True, BLACK)
        screen.blit(new_world_text, (new_world_button.x + 10, new_world_button.y + 10))
        pygame.draw.rect(screen, GRAY, load_world_button)
        load_world_text = font.render("Load World", True, BLACK)
        screen.blit(load_world_text, (load_world_button.x + 10, load_world_button.y + 10))
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
