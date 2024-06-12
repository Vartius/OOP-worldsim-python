from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from worldsim.world.World import World


class Organism(ABC):

    def __init__(self, world: "World", x, y):
        self.strength = 0
        self.initiative = 0
        self.x = x
        self.y = y
        self.world = world
        self.alive = True
        self.name = ""
        self.spawnAge = world.getTurn()

    def getStrength(self):
        return self.strength

    def setStrength(self, strength):
        self.strength = strength

    def getInitiative(self):
        return self.initiative

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getName(self):
        return self.name

    def getSpawnAge(self):
        return self.spawnAge

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setAlive(self, alive):
        self.alive = alive

    def getAlive(self):
        return self.alive

    def setSpawnAge(self, spawnAge):
        self.spawnAge = spawnAge

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def collision(self, inny):
        pass

    @abstractmethod
    def draw(self):
        pass
