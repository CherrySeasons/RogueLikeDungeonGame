import random
import numpy as np
import pygame
from game.logs import Logs

TILE_SIZE = 20

COLOR_WALL = (30, 30, 30)
COLOR_FLOOR = (70, 70, 70)
COLOR_PLAYER = (50, 200, 50)
COLOR_ENEMY = (200, 50, 50)

class Dungeon:
    WALL = '#'
    FLOOR = '.'

    def __init__(self, width=40, height=30, num_rooms=8):
        self.width = width
        self.height = height
        self.num_rooms = num_rooms
        self.grid = np.full((height, width), self.WALL)
        self.rooms = []
        self.generate_rooms()
        Logs.write("Dungeon generated successfully.")

    def generate_rooms(self):
        for _ in range(self.num_rooms):
            w, h = random.randint(5, 10), random.randint(4, 8)
            x, y = random.randint(1, self.width - w - 1), random.randint(1, self.height - h - 1)

            if not self.is_overlapping(x, y, w, h):
                self.create_room(x, y, w, h)

                center_x = x + w // 2
                center_y = y + h // 2

                # Connect to previous room
                if self.rooms:
                    prev_room = (self.rooms[-1][0] // TILE_SIZE, self.rooms[-1][1] // TILE_SIZE)
                    self.connect_rooms(prev_room, (center_x, center_y))

                # store room center in pixels
                self.rooms.append((center_x * TILE_SIZE, center_y * TILE_SIZE))

    def is_overlapping(self, x, y, w, h):
        for room in self.rooms:
            rx, ry = room
            rx, ry = rx // TILE_SIZE, ry // TILE_SIZE
            if abs(rx - x) < w and abs(ry - y) < h:
                return True
        return False

    def create_room(self, x, y, w, h):
        self.grid[y:y+h, x:x+w] = self.FLOOR

    def connect_rooms(self, room1, room2):
        x1, y1 = room1
        x2, y2 = room2
        if random.choice([True, False]):
            self.create_h_tunnel(x1, x2, y1)
            self.create_v_tunnel(y1, y2, x2)
        else:
            self.create_v_tunnel(y1, y2, x1)
            self.create_h_tunnel(x1, x2, y2)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.grid[y, x] = self.FLOOR

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.grid[y, x] = self.FLOOR

    @staticmethod
    def draw_health_bar(screen, entity, TILE_SIZE=20):
        BAR_WIDTH = TILE_SIZE
        BAR_HEIGHT = 5
        x = entity.x
        y = entity.y - BAR_HEIGHT - 2
        ratio = max(entity.health, 0) / entity.max_health
        pygame.draw.rect(screen, (255, 0, 0), (x, y, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, BAR_WIDTH * ratio, BAR_HEIGHT))

    @staticmethod
    def draw_dungeon(screen, dungeon, player, enemies, fog_radius=5):
        player_tile_x = int(player.x // TILE_SIZE)
        player_tile_y = int(player.y // TILE_SIZE)

        # Draw tiles
        for y in range(dungeon.height):
            for x in range(dungeon.width):
                color = COLOR_WALL if dungeon.grid[y, x] == '#' else COLOR_FLOOR
                distance = abs(player_tile_x - x) + abs(player_tile_y - y)
                if distance > fog_radius:
                    color = (color[0]//3, color[1]//3, color[2]//3)
                pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Draw player
        pygame.draw.rect(screen, COLOR_PLAYER, (player.x, player.y, TILE_SIZE, TILE_SIZE))

        # Draw enemies
        for e in enemies:
            if e.health > 0:
                enemy_tile_x = int(e.x // TILE_SIZE)
                enemy_tile_y = int(e.y // TILE_SIZE)
                distance = abs(player_tile_x - enemy_tile_x) + abs(player_tile_y - enemy_tile_y)
                if distance <= fog_radius:
                    pygame.draw.rect(screen, COLOR_ENEMY, (e.x, e.y, TILE_SIZE, TILE_SIZE))
                    Dungeon.draw_health_bar(screen, e)
