import random
from game.logs import Logs
TILE_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Enemy:
    def __init__(self, name="Goblin", health=60, attack=10, max_health=60,
                 velx=None, vely=None):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.x = 0
        self.y = 0
        self.vx = velx if velx is not None else random.randint(40,80) * random.choice([-1,1])
        self.vy = vely if vely is not None else random.randint(40,80) * random.choice([-1,1])
        self.wall_x = 0
        self.wall_y = 0

    def update(self, dt, dungeon):
        # Predict next position (do NOT move yet)
        next_x = self.x + self.vx * dt
        next_y = self.y + self.vy * dt

        # Compute current and next tile indices safely
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)
        next_tile_x = int(next_x // TILE_SIZE)
        next_tile_y = int(next_y // TILE_SIZE)

        # --- Keep inside screen bounds (for safety) ---
        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx)
        elif self.x + TILE_SIZE > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - TILE_SIZE
            self.vx = -abs(self.vx)

        if self.y < 0:
            self.y = 0
            self.vy = abs(self.vy)
        elif self.y + TILE_SIZE > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - TILE_SIZE
            self.vy = -abs(self.vy)

        # --- Horizontal collision ---
        if self.vx > 0 and dungeon.grid[tile_y, next_tile_x+1] == '#':
            self.x = next_tile_x * TILE_SIZE
            self.vx = -abs(self.vx)
        else:
            if 0 <= next_tile_x < dungeon.width:
                if dungeon.grid[tile_y, next_tile_x] == '#':
                    self.vx = -self.vx
                else:
                    self.x = next_x
            else:
                # Hit map boundary
                self.vx = -self.vx

        # --- Vertical collision ---
        if self.vy > 0 and dungeon.grid[next_tile_y+1, tile_x] == '#':
            self.y = next_tile_y * TILE_SIZE
            self.vy = -abs(self.vy)
        else:
            if 0 <= next_tile_y < dungeon.height:
                if dungeon.grid[next_tile_y, tile_x] == '#':
                    self.vy = -self.vy
                else:
                    self.y = next_y
            else:
                # Hit map boundary
                self.vy = -self.vy


    def attack_player(self, player):
        from random import randint, random
        if random() < 0.7:
            damage = randint(self.attack-2, self.attack+2)
            Logs.write(f"{self.name} attacks {player.name} for {damage} damage.")
            player.take_damage(damage)
        else:
            Logs.write(f"{self.name} missed {player.name}!")

    def take_damage(self, amount):
        self.health -= amount
        Logs.write(f"{self.name} takes {amount} damage. Health = {self.health}")
        if self.health <= 0:
            Logs.write(f"{self.name} has been defeated!")
