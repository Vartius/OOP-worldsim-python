import random
import json
from typing import List, Tuple, Optional, Union, TYPE_CHECKING
from worldsim.organisms.animals.Wolf import Wolf
from worldsim.organisms.animals.Human import Human
from worldsim.organisms.animals.Sheep import Sheep
from worldsim.organisms.animals.Fox import Fox
from worldsim.organisms.animals.Turtle import Turtle
from worldsim.organisms.animals.Antelope import Antelope
from worldsim.organisms.plants.Grass import Grass
from worldsim.organisms.plants.Dandelion import Dandelion
from worldsim.organisms.plants.Guarana import Guarana
from worldsim.organisms.plants.DeadlyNightshade import DeadlyNightshade
from worldsim.organisms.plants.Hogweed import Hogweed

if TYPE_CHECKING:
    from windowManager.Winman import WindowManager


class World:
    def __init__(self):
        self.world_size_x: int = -1
        self.world_size_y: int = -1
        self.organisms_count: int = -1
        self.organisms: List[
            Union[
                Wolf,
                Human,
                Sheep,
                Fox,
                Turtle,
                Antelope,
                Grass,
                Dandelion,
                Guarana,
                DeadlyNightshade,
                Hogweed,
            ]
        ] = []
        self.organisms_grid: List[
            List[
                Optional[
                    Union[
                        Wolf,
                        Human,
                        Sheep,
                        Fox,
                        Turtle,
                        Antelope,
                        Grass,
                        Dandelion,
                        Guarana,
                        DeadlyNightshade,
                        Hogweed,
                    ]
                ]
            ]
        ] = []
        self.turn: int = 0
        self.human_turn: bool = False
        self.windowManager: Optional["WindowManager"] = None
        self.special_ability_used: bool = False

    def setWindowManager(self, windowManager: "WindowManager") -> None:
        self.windowManager = windowManager

    def getEmptyPositions(self) -> List[Tuple[int, int]]:
        empty_positions: List[Tuple[int, int]] = []
        for i in range(self.world_size_x):
            for j in range(self.world_size_y):
                if self.organisms_grid[i][j] is None:
                    empty_positions.append((i, j))
        return empty_positions

    def addOrganismByDraw(self, x: int, y: int, draw: str) -> None:
        organism: Union[
            Wolf,
            Human,
            Sheep,
            Fox,
            Turtle,
            Antelope,
            Grass,
            Dandelion,
            Guarana,
            DeadlyNightshade,
            Hogweed,
        ]
        if self.organisms_grid[x][y] is not None:
            org = self.getOrganismAt(x, y)
            if org is not None:
                self.removeOrganism(org)
                self.addLog("Removed " + org.getName() + " at " + str(x) + " " + str(y))
        self.addLog("Added " + draw + " at " + str(x) + " " + str(y))
        if draw == "W":
            organism = Wolf(self, x, y)
        elif draw == "H":
            organism = Human(self, x, y)
        elif draw == "S":
            organism = Sheep(self, x, y)
        elif draw == "F":
            organism = Fox(self, x, y)
        elif draw == "T":
            organism = Turtle(self, x, y)
        elif draw == "A":
            organism = Antelope(self, x, y)
        elif draw == "G":
            organism = Grass(self, x, y)
        elif draw == "D":
            organism = Dandelion(self, x, y)
        elif draw == "U":
            organism = Guarana(self, x, y)
        elif draw == "N":
            organism = DeadlyNightshade(self, x, y)
        elif draw == "O":
            organism = Hogweed(self, x, y)

        self.organisms.append(organism)
        self.organisms_grid[x][y] = organism
        if self.windowManager:
            self.windowManager.updateButton(x, y, draw)

    def initWorld(
        self, world_size_x: int, world_size_y: int, organisms_count: int
    ) -> None:
        self.world_size_x = world_size_x
        self.world_size_y = world_size_y
        self.organisms_count = organisms_count
        self.organisms_grid = [
            [None for _ in range(self.world_size_x)] for _ in range(self.world_size_y)
        ]
        empty_positions = self.getEmptyPositions()
        random.shuffle(empty_positions)
        self.addOrganismByDraw(empty_positions[0][0], empty_positions[0][1], "H")
        for i in range(1, self.organisms_count):
            self.addOrganismByDraw(
                empty_positions[i][0],
                empty_positions[i][1],
                random.choice(["W", "S", "F", "T", "A", "G", "D", "U", "N", "O"]),
            )
        self.nextTurn()

    def getOrganisms(
        self,
    ) -> List[
        Union[
            "Wolf",
            "Human",
            "Sheep",
            "Fox",
            "Turtle",
            "Antelope",
            "Grass",
            "Dandelion",
            "Guarana",
            "DeadlyNightshade",
            "Hogweed",
        ]
    ]:
        return self.organisms

    def getWorldSizeX(self) -> int:
        return self.world_size_x

    def getWorldSizeY(self) -> int:
        return self.world_size_y

    def getOrganismsCount(self) -> int:
        return self.organisms_count

    def deadifyOrganism(
        self,
        organism: Union[
            "Wolf",
            "Human",
            "Sheep",
            "Fox",
            "Turtle",
            "Antelope",
            "Grass",
            "Dandelion",
            "Guarana",
            "DeadlyNightshade",
            "Hogweed",
        ],
    ) -> None:
        if isinstance(organism, Human):
            self.gameOver("You died")
            return
        organism.setAlive(False)
        x, y = organism.getX(), organism.getY()
        self.organisms_grid[x][y] = None

    def clearOrganisms(self) -> None:
        self.organisms = []
        self.organisms_grid = [
            [None for _ in range(self.world_size_x)] for _ in range(self.world_size_y)
        ]

    def moveOrganism(
        self,
        organism: Union[
            "Wolf",
            "Human",
            "Sheep",
            "Fox",
            "Turtle",
            "Antelope",
            "Grass",
            "Dandelion",
            "Guarana",
            "DeadlyNightshade",
            "Hogweed",
        ],
        x: int,
        y: int,
    ) -> None:
        old_x, old_y = organism.getX(), organism.getY()
        self.organisms_grid[old_x][old_y] = None
        self.organisms_grid[x][y] = organism
        organism.setX(x)
        organism.setY(y)

    def sortOrganisms(self) -> None:
        self.organisms.sort(key=lambda x: x.getInitiative(), reverse=True)
        self.organisms.sort(key=lambda x: x.getSpawnAge(), reverse=True)

    def removeOrganism(
        self,
        organism: Union[
            "Wolf",
            "Human",
            "Sheep",
            "Fox",
            "Turtle",
            "Antelope",
            "Grass",
            "Dandelion",
            "Guarana",
            "DeadlyNightshade",
            "Hogweed",
        ],
    ) -> None:
        self.organisms.remove(organism)

    def nextTurn(self) -> None:
        self.turn += 1
        self.sortOrganisms()
        for organism in self.organisms:
            if organism.getAlive():
                organism.action()

        for organism in self.organisms:
            if not organism.getAlive():
                if isinstance(organism, Human):
                    self.gameOver("You died")
                    return
                self.removeOrganism(organism)
        organisms_count = {}
        for organism in self.organisms:
            if organism.getName() in organisms_count:
                organisms_count[organism.getName()] += 1
            else:
                organisms_count[organism.getName()] = 1
        for key in organisms_count:
            if organisms_count[key] > self.world_size_x * self.world_size_y / 3:
                self.gameOver("Overpopulation of " + key)
                return
        if self.windowManager:
            self.windowManager.updateButtons()

    def getOrganismAt(self, x: int, y: int) -> Optional[
        Union[
            Wolf,
            Human,
            Sheep,
            Fox,
            Turtle,
            Antelope,
            None,
            Grass,
            Dandelion,
            Guarana,
            DeadlyNightshade,
            Hogweed,
        ]
    ]:
        return self.organisms_grid[x][y]

    def getTurn(self):
        return self.turn

    def startHumanTurn(self) -> None:
        self.human_turn = True
        if self.windowManager:
            self.windowManager.enableHumanControls()

    def handleHumanMove(self, direction: str) -> None:
        human = next((org for org in self.organisms if isinstance(org, Human)), None)
        if not human:
            return
        moves = {"W": (-1, 0), "A": (0, -1), "S": (1, 0), "D": (0, 1)}
        if direction in moves:
            human.move(moves[direction][0], moves[direction][1])
            if self.special_ability_used:
                self.human_turn = True
                self.special_ability_used = False
                if self.windowManager:
                    self.windowManager.enableHumanControls()
            else:
                self.human_turn = False
                self.nextTurn()
        else:
            if direction == "E":
                human.specialAbility()
            elif direction == "Q":
                if self.windowManager:
                    self.windowManager.close()
            elif direction == "Y":
                self.saveGame()
            elif direction == "L":
                self.loadGame()
            self.human_turn = True
            if self.windowManager:
                self.windowManager.enableHumanControls()

    def isInField(self, x: int, y: int) -> bool:
        return 0 <= x < self.world_size_x and 0 <= y < self.world_size_y

    def saveGame(self) -> None:
        human = next((org for org in self.organisms if isinstance(org, Human)), None)
        if not human:
            return
        if self.windowManager:
            self.windowManager.addLog("Saving game...")
        data = {
            "world_size_x": self.world_size_x,
            "world_size_y": self.world_size_y,
            "organisms_count": self.organisms_count,
            "turn": self.turn,
            "human_turn": self.human_turn,
            "special_ability_used": self.special_ability_used,
            "organisms": [
                [
                    org.getX(),
                    org.getY(),
                    org.getAlive(),
                    org.getSpawnAge(),
                    org.getStrength(),
                    org.draw(),
                ]
                for org in self.organisms
                if not isinstance(org, Human)
            ],
            "human": [
                human.getX(),
                human.getY(),
                human.getAlive(),
                human.getSpawnAge(),
                human.getStrength(),
                human.getCooldown(),
                human.getSpecialAbilityCounter(),
            ],
            "logs": self.windowManager.getLogs() if self.windowManager else "",
        }

        json_data = json.dumps(data, indent=4)
        with open("save.json", "w") as file:
            file.write(json_data)

    def addOrganismWithParametrs(
        self,
        x: int,
        y: int,
        alive: bool,
        spawnAge: int,
        strength: int,
        draw: str,
        cooldown: int,
        specialAbilityCounter: int,
    ) -> None:
        organism: Union[
            Wolf,
            Human,
            Sheep,
            Fox,
            Turtle,
            Antelope,
            Grass,
            Dandelion,
            Guarana,
            DeadlyNightshade,
            Hogweed,
        ]
        if draw == "W":
            organism = Wolf(self, x, y)
        elif draw == "H":
            organism = Human(self, x, y)
            organism.setCooldown(cooldown)
            organism.setSpecialAbilityCounter(specialAbilityCounter)
        elif draw == "S":
            organism = Sheep(self, x, y)
        elif draw == "F":
            organism = Fox(self, x, y)
        elif draw == "T":
            organism = Turtle(self, x, y)
        elif draw == "A":
            organism = Antelope(self, x, y)
        elif draw == "G":
            organism = Grass(self, x, y)
        elif draw == "D":
            organism = Dandelion(self, x, y)
        elif draw == "U":
            organism = Guarana(self, x, y)
        elif draw == "N":
            organism = DeadlyNightshade(self, x, y)
        elif draw == "O":
            organism = Hogweed(self, x, y)

        organism.setAlive(alive)
        organism.setSpawnAge(spawnAge)
        organism.setStrength(strength)

        self.organisms.append(organism)
        self.organisms_grid[x][y] = organism
        if self.windowManager:
            self.windowManager.updateButton(x, y, draw)

    def loadOrganisms(self, data: dict) -> None:
        for org in data["organisms"]:
            self.addOrganismWithParametrs(
                org[0], org[1], org[2], org[3], org[4], org[5], 0, 0
            )
        self.addOrganismWithParametrs(
            data["human"][0],
            data["human"][1],
            data["human"][2],
            data["human"][3],
            data["human"][4],
            "H",
            data["human"][5],
            data["human"][6],
        )

    def loadGame(self) -> None:
        if self.windowManager:
            self.windowManager.addLog("Loading game...")
        with open("save.json", "r") as file:
            data = json.load(file)
        self.world_size_x = data["world_size_x"]
        self.world_size_y = data["world_size_y"]
        self.organisms_count = data["organisms_count"]
        self.turn = data["turn"]
        self.human_turn = data
        self.special_ability_used = data["special_ability_used"]
        self.clearOrganisms()
        self.loadOrganisms(data)
        if self.windowManager:
            self.windowManager.resetGame(data)

    def addLog(self, log: str) -> None:
        if self.windowManager:
            self.windowManager.addLog(log)
        pass

    def gameOver(self, msg) -> None:
        if self.windowManager:
            self.windowManager.gameOver(msg)

    def setSpecialAbilityUsed(self, used: bool) -> None:
        self.special_ability_used = used
