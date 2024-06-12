import random
from worldsim.organisms.animals.Animal import Animal


class Antelope(Animal):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.strength = 4
        self.initiative = 4
        self.name = "Antelope"

    def action(self):
        moves = [
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]
        move = random.choice(moves)
        new_x = self.x + move[0]
        new_y = self.y + move[1]
        if self.world.isInField(new_x, new_y):
            other = self.world.getOrganismAt(new_x, new_y)
            if other is None:
                self.world.moveOrganism(self, new_x, new_y)
            else:
                other.collision(self)

    def collision(self, other):
        if random.random() < 0.5 and other.name != self.name:
            self.world.addLog(self.name + " escaped from " + other.name)
            self.action()
        else:
            super().collision(other)

    def draw(self):
        return "A"
