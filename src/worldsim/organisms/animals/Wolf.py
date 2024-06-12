from worldsim.organisms.animals.Animal import Animal


class Wolf(Animal):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.strength = 9
        self.initiative = 5
        self.name = "Wolf"

    def draw(self):
        return "W"
