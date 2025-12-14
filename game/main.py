import pygame
from game.dungeon import Dungeon
from game.player import Player
from game.enemy import Enemy
from game.logs import Logs

TILE_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🕹️ 2D Roguelike Dungeon")
    clock = pygame.time.Clock()

    Logs.clear()
    Logs.write("=== New Game Started ===")

    # Create dungeon and player
    dungeon = Dungeon(width=40, height=30, num_rooms=8)
    player = Player("Arkon")
    player.x, player.y = dungeon.rooms[0]

    # Spawn enemies in rooms
    enemies = [Enemy(name=f"Goblin{i+1}") for i in range(4)]
    for i, e in enumerate(enemies):
        room_index = (i + 1) % len(dungeon.rooms)
        e.x, e.y = dungeon.rooms[room_index]

    speed = 120  # pixels/sec
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: dy = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dy = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dx = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx = 1

        new_x = player.x + dx * speed * dt
        new_y = player.y + dy * speed * dt
        tile_x = int(new_x // TILE_SIZE)
        tile_y = int(new_y // TILE_SIZE)

        # Check for floor before moving
        if 0 <= tile_x < dungeon.width and 0 <= tile_y < dungeon.height:
            switch = 1
            if dx == 1:
                if dungeon.grid[tile_y, tile_x] == '.' and dungeon.grid[tile_y, tile_x+1] == '#':
                    player.x, player.y = tile_x*TILE_SIZE, new_y
                    Logs.write(f"{player.name} moves to ({player.x:.1f}, {player.y:.1f})")
                    switch = 0
            if dy == 1:
                if dungeon.grid[tile_y, tile_x] == '.' and dungeon.grid[tile_y+1, tile_x] == '#':
                    player.x, player.y = new_x, tile_y*TILE_SIZE
                    Logs.write(f"{player.name} moves to ({player.x:.1f}, {player.y:.1f})")  
                    switch = 0
            
            if switch == 1:                                      
                if dungeon.grid[tile_y, tile_x] == '.':
                    player.x, player.y = new_x, new_y
                    Logs.write(f"{player.name} moves to ({player.x:.1f}, {player.y:.1f})")

        # Update enemies
        for e in enemies:
            if e.health <= 0:
                continue
            try:
                e.update(dt, dungeon)
            except Exception as ex:
                print(f"ERROR updating {e.name} : {ex}")
                raise

            # Enemy attacks player if close
            if abs(e.x - player.x) <= TILE_SIZE and abs(e.y - player.y) <= TILE_SIZE:
                e.attack_player(player)

        # Player attacks enemies if close
        for e in enemies:
            if abs(e.x - player.x) <= TILE_SIZE and abs(e.y - player.y) <= TILE_SIZE:
                player.attack_enemy(e)

        # Draw everything
        screen.fill((0, 0, 0))
        Dungeon.draw_dungeon(screen, dungeon, player, enemies)
        Dungeon.draw_health_bar(screen, player)
        pygame.display.flip()

        # Check win/lose conditions
        if player.health <= 0:
            Logs.write("Player died. Game Over.")
            running = False
        if all(e.health <= 0 for e in enemies):
            Logs.write("All enemies defeated. Victory!")
            running = False

    pygame.quit()
    Logs.write("=== Game Ended ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"ERROR occured : {ex}")
        raise
