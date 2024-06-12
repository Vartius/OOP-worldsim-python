from worldsim.organisms.Organism import Organism

from abc import ABC
import random


class Animal(Organism, ABC):
    def action(self):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        move = random.choice(moves)
        new_x = self.x + move[0]
        new_y = self.y + move[1]
        if self.world.isInField(new_x, new_y):
            other = self.world.getOrganismAt(new_x, new_y)
            if other is None:
                self.world.moveOrganism(self, new_x, new_y)  # type: ignore
            else:
                other.collision(self)

    def reproduce(self):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(moves)
        for move in moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            if self.world.isInField(new_x, new_y):
                counter = 0
                for _ in moves:
                    test_x = new_x + _[0]
                    test_y = new_y + _[1]
                    if self.world.isInField(test_x, test_y):
                        if self.world.getOrganismAt(test_x, test_y) is not None:
                            counter += 1
                if counter > 2 and abs(random.random()) > 0.2:
                    continue
                other = self.world.getOrganismAt(new_x, new_y)
                if other is None:
                    self.world.addLog(self.name + " reproduced")
                    self.world.addOrganismByDraw(new_x, new_y, self.draw())

    def collision(self, other):
        if other.name == self.name:
            if (
                self.world.getTurn() - self.getSpawnAge() > 5
                and self.world.getTurn() - other.getSpawnAge() > 5
            ):
                self.reproduce()
        elif other.strength > self.strength:
            self.world.addLog(other.name + " killed " + self.name)
            new_x = self.x
            new_y = self.y
            self.world.moveOrganism(other, new_x, new_y)
            self.world.deadifyOrganism(self)  # type: ignore
        else:
            self.world.addLog(self.name + " killed " + other.name)
            new_x = other.x
            new_y = other.y
            self.world.deadifyOrganism(other)

    def draw(self):
        return "Bruh"
