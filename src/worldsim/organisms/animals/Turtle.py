from worldsim.organisms.animals.Animal import Animal
import random


class Turtle(Animal):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.strength = 2
        self.initiative = 1
        self.name = "Turtle"

    def action(self):
        if random.random() < 0.25:
            super().action()

    def collision(self, other):
        if other.strength >= 5:
            super().collision(other)
        else:
            self.world.addLog(self.name + " blocked " + other.name + "'s attack")

    def draw(self):
        return "T"
