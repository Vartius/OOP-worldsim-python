from worldsim.organisms.animals.Animal import Animal
import random


class Fox(Animal):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.strength = 3
        self.initiative = 7
        self.name = "Fox"
        self.position = (x, y)

    def action(self):
        moves = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]
        random.shuffle(moves)
        for move in moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            if self.world.isInField(new_x, new_y):
                other = self.world.getOrganismAt(new_x, new_y)
                if other is None:
                    self.world.moveOrganism(self, new_x, new_y)
                    break
                elif other.strength <= self.strength:
                    other.collision(self)
                    break

    def draw(self):
        return "F"
