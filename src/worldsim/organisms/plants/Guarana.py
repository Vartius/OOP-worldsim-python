from worldsim.organisms.plants.Plant import Plant


class Guarana(Plant):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.name = "Guarana"

    def collision(self, other):
        super().collision(other)
        other.setStrength(other.getStrength() + 3)

    def draw(self):
        return "U"
