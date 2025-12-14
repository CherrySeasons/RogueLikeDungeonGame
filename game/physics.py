# physics.py
from game.logs import Logs

class Physics:
    @staticmethod
    def resolve_attack(attacker, defender):
        damage = max(attacker.attack - getattr(defender, "defense", 0), 0)
        defender.take_damage(damage)
        Logs.write(f"{attacker.name} dealt {damage} to {defender.name}.")
