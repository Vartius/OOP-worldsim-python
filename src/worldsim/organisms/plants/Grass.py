from worldsim.organisms.plants.Plant import Plant


class Grass(Plant):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.name = "Grass"

    def draw(self):
        return "G"
