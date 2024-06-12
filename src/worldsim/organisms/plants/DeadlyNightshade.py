from worldsim.organisms.plants.Plant import Plant


class DeadlyNightshade(Plant):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.name = "Deadly Nightshade"
        self.strength = 99

    def collision(self, other):
        super().collision(other)
        self.world.deadifyOrganism(other)  # type: ignore

    def draw(self):
        return "N"
