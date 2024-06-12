from worldsim.organisms.Organism import Organism
from abc import ABC
import random


class Plant(Organism, ABC):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.strength = 0
        self.initiative = 0

    def reproduce(self):
        if random.random() > 0.01:
            return
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(moves)
        for move in moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            if self.world.isInField(new_x, new_y):
                other = self.world.getOrganismAt(new_x, new_y)
                if other is None:
                    self.world.addLog(self.name + " reproduced")
                    self.world.addOrganismByDraw(new_x, new_y, self.draw())
                    break

    def action(self):
        self.reproduce()

    def collision(self, other):
        if other.strength > self.strength:
            self.world.addLog(other.name + " killed " + self.name)
            self.world.deadifyOrganism(self)  # type: ignore
            new_x = self.x
            new_y = self.y
            self.world.moveOrganism(other, new_x, new_y)
        else:
            self.world.addLog(self.name + " killed " + other.name)
            self.world.deadifyOrganism(other)

    def draw(self):
        return "Bruh"
