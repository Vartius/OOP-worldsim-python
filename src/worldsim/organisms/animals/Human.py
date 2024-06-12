# Human.py
import random
from .Animal import Animal


class Human(Animal):
    def __init__(self, world, x: int, y: int):
        super().__init__(world, x, y)
        self.strength = 5
        self.initiative = 4
        self.name = "Human"
        self.cooldown = 0
        self.special_ability_counter = 0

    def action(self) -> None:
        self.world.startHumanTurn()
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.special_ability_counter > 0:
            if self.special_ability_counter > 2:
                self.make_two_moves()
            else:
                if random.random() < 0.5:
                    self.make_two_moves()
                else:
                    self.make_one_move()
            self.special_ability_counter -= 1
        else:
            self.make_one_move()

    def make_one_move(self):
        self.world.startHumanTurn()

    def make_two_moves(self):
        if self.special_ability_counter > 0:
            self.world.setSpecialAbilityUsed(True)
        self.make_one_move()

    def move(self, dx: int, dy: int) -> None:
        new_x, new_y = self.getX() + dx, self.getY() + dy
        if self.world.isInField(new_x, new_y):
            other = self.world.getOrganismAt(new_x, new_y)
            if other is None:
                self.world.moveOrganism(self, new_x, new_y)
            else:
                other.collision(self)
        if self.world.windowManager:
            self.world.windowManager.updateButtons()

    def specialAbility(self) -> None:
        if self.cooldown == 0:
            self.cooldown = 5
            self.special_ability_counter = 5  # Next 5 turns affected
            self.world.addLog("Human used special ability(Antelope's speed)")
        else:
            self.world.addLog("Human's special ability is on cooldown")

    def collision(self, other: "Animal") -> None:
        if other.strength > self.strength:
            self.world.addLog(other.name + " killed " + self.name)
            self.world.deadifyOrganism(self)
        else:
            self.world.addLog(self.name + " killed " + other.name)
            self.world.moveOrganism(self, other.getX(), other.getY())
            self.world.deadifyOrganism(other)  # type: ignore

    def draw(self) -> str:
        return "H"

    def getCooldown(self) -> int:
        return self.cooldown

    def getSpecialAbilityCounter(self) -> int:
        return self.special_ability_counter

    def setCooldown(self, cooldown: int) -> None:
        self.cooldown = cooldown

    def setSpecialAbilityCounter(self, special_ability_counter: int) -> None:
        self.special_ability_counter = special_ability_counter
