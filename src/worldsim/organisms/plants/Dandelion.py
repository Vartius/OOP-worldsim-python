from worldsim.organisms.plants.Plant import Plant


class Dandelion(Plant):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.name = "Dandelion"

    def action(self):
        for i in range(3):
            self.reproduce()

    def draw(self):
        return "D"
