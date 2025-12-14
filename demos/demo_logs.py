# demo_logs.py
from game.logs import Logs

def main():
    logger = Logs()

    logger.log_enter_dungeon(1)
    logger.log_move("Hero", 5, 7)
    logger.log_encounter("Hero", "Goblin", enemy=1)
    logger.log_attack("Hero", "Goblin", 12)
    logger.log_defend("Goblin", 4)
    logger.log_dodge("Hero")
    logger.log_pickup("Hero", "Health Potion")
    logger.log_encounter("Hero", "Dark Corridor")
    logger.log_explore("Hero", "Dark Corridor")
    logger.log_game_over()

if __name__ == "__main__":
    main()
