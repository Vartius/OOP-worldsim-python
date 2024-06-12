from worldsim.organisms.animals.Animal import Animal
from worldsim.organisms.plants.Plant import Plant


class Hogweed(Plant):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.name = "Hogweed"
        self.strength = 10

    def collision(self, other):
        super().collision(other)
        self.world.deadifyOrganism(other)  # type: ignore

    def action(self):
        moves = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for move in moves:
            x = self.x + move[0]
            y = self.y + move[1]
            if self.world.isInField(x, y):
                organism = self.world.getOrganismAt(x, y)
                if organism is not None and isinstance(organism, Animal):
                    self.world.deadifyOrganism(organism)

    def draw(self):
        return "O"
