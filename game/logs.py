import datetime
import os

class Logs:
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")  # parent of game/
    LOG_FILE = os.path.join(LOG_DIR, "logs.txt")

    @classmethod
    def _ensure_dir(cls):
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)

    @classmethod
    def write(cls, message):
        cls._ensure_dir()
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        with open(cls.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {message}\n")

    @classmethod
    def clear(cls):
        """Clear logs before starting a new game."""
        cls._ensure_dir()
        with open(cls.LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")  # empty file
