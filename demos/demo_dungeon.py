# demo_dungeon.py
from game.dungeon import Dungeon

def main():
    print("🧭 Generating Procedural Dungeon...\n")

    # Create a dungeon instance
    dungeon = Dungeon(width=80, height=50, num_rooms=12)

    # Display the dungeon layout
    dungeon.display()

    print("\n✅ Dungeon generation complete!")
    print(f"Total rooms generated: {len(dungeon.rooms)}")

    # Optionally, show room center coordinates
    print("\nRoom Centers:")
    for i, (x, y) in enumerate(dungeon.rooms, start=1):
        print(f"  Room {i}: Center at ({x}, {y})")

if __name__ == "__main__":
    main()
