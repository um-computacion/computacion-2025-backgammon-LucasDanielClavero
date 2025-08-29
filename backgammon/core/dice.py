import random
class Dice:
    def __init__(self):
        self._values_ = []

    def roll(self) -> list[int]:
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self._values_ = [die1, die2]
        return self._values_
    
    def get_moves(self) -> list[int]:
        if not self._values_:
            return []
        die1, die2 = self._values_
        if die1 == die2:
            return [die1] * 4
        else:
            return [die1, die2]