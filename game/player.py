# player.py
import random
from game.logs import Logs

class Player:
    def __init__(self, name="Hero", health=100, attack=15, defense=5, max_health=100):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack = attack
        self.defense = defense
        self.x = 0
        self.y = 0

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 3, self.attack + 3)
        Logs.write(f"{self.name} attacks {enemy.name} for {damage} damage.")
        enemy.take_damage(damage)

    def take_damage(self, amount):
        self.health -= amount
        Logs.write(f"{self.name} takes {amount} damage! Health = {self.health}")
        if self.health <= 0:
            Logs.write(f"{self.name} has fallen!")
