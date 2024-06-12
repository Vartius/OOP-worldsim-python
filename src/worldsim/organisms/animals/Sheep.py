from worldsim.organisms.animals.Animal import Animal


class Sheep(Animal):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.strength = 3
        self.initiative = 7
        self.name = "Sheep"

    def draw(self):
        return "S"
