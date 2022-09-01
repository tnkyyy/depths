from random import randrange, randint, choice
import shutil  # Finding terminal size, for centering
from dataclasses import dataclass
from typing import Any
from pick import pick
import os
import math
import time


def printc(s):
    print(s.center(shutil.get_terminal_size().columns))


class Rank:
    def __init__(self, name, xpRequired, baseHP, baseAttack, baseDodge):
        self.name = name
        self.baseHP = baseHP
        self.baseAttack = baseAttack
        self.baseDodge = baseDodge
        self.xpRequired = xpRequired


# Ranks
ROOKIE = Rank("ROOKIE", 200, 100, 20, 2)
NOVICE = Rank("NOVICE", 300, 20, 5, 2)
CADET = Rank("CADET", 500, 25, 8, 2)
ADEPT = Rank("ADEPT", 700, 30, 8, 2)
MASTER = Rank("MASTER", 800, 25, 9, 2)
LEGEND = Rank("LEGEND", 1000, 50, 10, 2)
OVERLORD = Rank("OVERLORD", 9999, 75, 15, 3)


@dataclass
class ItemQueueEntry:
    itemName: str
    turnsTillExpiration: int
    effectCode: str
    secondaryEffectCode: Any
    effectStrength: int
    secondaryEffectStrength: Any


@dataclass
class Item:
    name: str
    description: str
    duration: int
    isOneOff: bool
    effect: str
    secondaryEffect: Any
    strength: int
    secondaryStrength: Any
    cost: float


# This will be moved to a different file later
items = [
    Item(
        "Bulwark",
        "Temporarily adds maximum health to bolster defence",
        15,
        False,
        "MAX",
        None,
        50,
        None,
        2.50,
    ),
    Item(
        "Stim",
        "Temporarily increases your dodge significantly but reduces your maximum health.",
        14,
        False,
        "DOD",
        "MAX",
        30,
        -25,
        4,
    ),
    Item(
        "Name Tag", "Allows you to change your name", "N/A", True, "NAM", None, 1, 1, 3
    ),
    Item(
        "Protein Powder",
        "Permanently boosts your maximum health by a small amount",
        "N/A",
        True,
        "MAX",
        None,
        20,
        None,
        1.00,
    ),
    Item(
        "Hand Grippers",
        "Permanently boosts your attack by a small amount",
        "N/A",
        True,
        "ATK",
        None,
        5,
        None,
        1.00,
    ),
    Item(
        "Titanium Vest",
        "Temporarily increases maximum health significantly but reduces dodge significantly",
        20,
        False,
        "MAX",
        "DOD",
        75,
        -20,
        7,
    ),
    Item(
        "Map",
        "Allows you to see the map layout of floors permanently",
        "N/A",
        True,
        "MAP",
        None,
        True,
        None,
        10,
    ),
]


def getItemDefinition(itemName):
    global items
    for item in items:
        if item.name == itemName:
            return item
    raise KeyError(f'No item with name "{itemName}"')


# Handling rankups
rankOrder = [ROOKIE, NOVICE, CADET, ADEPT, MASTER, LEGEND, OVERLORD]


class Player:
    def __init__(self):
        self.name = input("Enter your player's name: ")
        self.health: int = 100
        self.maxHealth: int = 100
        self.dodge: int = 2  # Base dodge is 2%
        self.gold: float = 0
        self.rank = ROOKIE
        self.xpToNextRank = rankOrder[rankOrder.index(self.rank)].xpRequired
        self.baseAttack = self.rank.baseAttack
        self.bonusAttack = 0
        self.inventory = []
        self.kills = 0
        self.currentFloor = 1
        self.itemQueue = []
        self.hasMap = False

    def gainXP(self, xpAmount):
        self.xpToNextRank -= xpAmount
        if self.xpToNextRank <= 0:
            self.rankUp()

    def gainGold(self, goldAmount):
        self.gold += goldAmount

    def changeHealth(self, nhealth):
        newHealth = self.health + nhealth
        self.health = min(
            newHealth, self.maxHealth
        )  # Clamp so health can't go above max

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
          self.endGame()

    def endGame(self):
      print(f'{self.name} perished!')
      time.sleep(1)
      print(f'You reached floor {self.currentFloor}')
      
    
    def changeName(self, defaultParameter):
        newName = ""
        while newName == "":
            newName = input("Enter a new name for your character: ")
            self.name = newName

    def changeMaxHealth(self, newMaxHealth):
        self.maxHealth += newMaxHealth
        self.health = min(self.health, self.maxHealth)

    def changeDodge(self, newDodge):
        newDodge = self.dodge + newDodge
        self.dodge = max(
            0, min(90, newDodge)
        )  # Clamp the values so that dodge doesn't get excessive or too low

    def changeGold(self, newGold):
        self.gold = newGold

    def changeBonusAttack(self, newBonusAttack):
        self.bonusAttack = newBonusAttack

    def findItem(self, itemCode):
        global getItemDefinition
        self.getItem(getItemDefinition(itemCode))

    def changeMapStatus(self, hasMap):
        self.hasMap = hasMap

    def rankUp(self):
        self.rank = rankOrder[rankOrder.index(self.rank) + 1]
        self.xpToNextRank = rankOrder[rankOrder.index(self.rank)].xpRequired
        print(
            f"\n{self.name} ranked up to {self.rank.name}! XP Required for next rank: {self.xpToNextRank}\n"
        )
        self.changeMaxHealth(self.maxHealth + self.rank.baseHP)
        print(f"{p.name}'s max HP increased by {self.rank.baseHP}")
        self.baseAttack += self.rank.baseAttack
        print(f"{p.name}'s attack increased by {self.rank.baseAttack}")
        self.changeDodge(self.dodge + self.rank.baseDodge)
        print(f"{p.name}'s dodge increased by {self.rank.baseDodge}")

    # THIS IS WHERE ITEM EFFECTS ARE DEFINED
    playerDispatch = {
        "NAM": changeName,
        "HEL": changeHealth,
        "MAX": changeMaxHealth,
        "DOD": changeDodge,
        "GOL": changeGold,
        "ATK": changeBonusAttack,
        "MAP": changeMapStatus,
    }

    def addKill(self):
        self.kills += 1

    def addFloor(self):
        self.currentFloor += 1

    def addEffect(self, effectCode, value):
        self.playerDispatch[effectCode](self, value)

    def removeEffect(self, effectCode, value):
        self.playerDispatch[effectCode](self, -value)

    def useItem(self, itemIndex):
        item = self.inventory.pop(itemIndex)
        self.addEffect(item.effect, item.strength)
        if item.secondaryEffect != None:
            self.addEffect(item.secondaryEffect, item.secondaryStrength)
        if item.isOneOff == False:
            self.itemQueue.append(
                ItemQueueEntry(
                    item.name,
                    item.duration,
                    item.effect,
                    item.secondaryEffect,
                    item.strength,
                    item.secondaryStrength,
                )
            )

    def itemQueueSweep(self):
        for item in self.itemQueue:
            if item.turnsTillExpiration == 1:
                if item.secondaryEffectCode != None:
                    self.removeEffect(
                        item.secondaryEffectCode, item.secondaryEffectStrength
                    )
                self.removeEffect(item.effectCode, item.effectStrength)
                print(f"{self.name}'s {item.itemName} expired!")
                self.itemQueue.pop(self.itemQueue.index(item))
            else:
                item.turnsTillExpiration -= 1

    def getItem(self, item):
        self.inventory.append(item)

    def newTurn(self):
        self.itemQueueSweep()

    def getItemIndexFromPrompt(self):
        promptArr = []
        returnPrompt = "--- Return ---"
        title = "Choose an item to use: "
        for item in self.inventory:
            promptArr.append(f"{item.name}: {item.description}")
        promptArr.append(returnPrompt)
        option, index = pick(promptArr, title)
        if option == returnPrompt:
            return None
        else:
            return index

    def useItemFlow(self):
        itemIndex = self.getItemIndexFromPrompt()
        if itemIndex != None:
            self.useItem(itemIndex)
        else:
            return


@dataclass
class EnemyInfo:
    name: str
    attack: int
    health: int
    maxHealth: int
    dodge: int
    xpGiven: int
    goldGiven: float


enemyList = [
    EnemyInfo("Goblin", 5, 30, 30, 1, 15, 0.1),
    EnemyInfo("Armoured Goblin", 3, 50, 50, 0, 25, 0.2),
    EnemyInfo("Striker Goblin", 7, 20, 20, 10, 10, 0.1),
]


def getEnemyDefinition(enemyName):
    global enemyList
    for enemy in enemyList:
        if enemy.name == enemyName:
            return enemy
    raise KeyError(f'No enemy with name "{enemyName}"')


@dataclass
class Encounter:
    enemies: list
    minLevel: int
    id: str


encounterList = [
    Encounter(["Goblin", "Goblin"], 1, "Goblin Gang"),
    Encounter(["Armoured Goblin"], 1, "Goblin Guard"),
    Encounter(["Armoured Goblin", "Striker Goblin"], 2, "Father and Son"),
]


def getRandomEncounterOfLevel(minLevel):
    e = choice(encounterList)
    while e.minLevel > minLevel:
        e = choice(encounterList)

    return e


def hasDodged(e) -> bool:  # e -> entity
    # We need to refer to the global variable of the player
    # Generates a random integer between 0 and 100 inclusive
    dodgeValue = randrange(101)
    # The greater the player dodge, the more likely that this evaluates to true
    # We can just return the expression as it will evaluate to true or false itself
    return dodgeValue <= e.dodge


class Coords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(c1, c2):  # So we can add coordinates together for handling movement
        return Coords(c1.x + c2.x, c1.y + c2.y)


basisDict = {
    "Up": Coords(0, -1),
    "Down": Coords(0, 1),
    "Right": Coords(1, 0),
    "Left": Coords(-1, 0),
}
usedCoords = []


# We need to ensure that duplicate coords are not present, naive approach so I'll have a look later
def generateCoords(range):
    global usedCoords
    newCoord = Coords(randint(0, range - 1), randint(0, range - 1))
    while True:
        valid = True
        for item in usedCoords:
            if item.x == newCoord.x and item.y == newCoord.y:
                valid = False
        if valid:
            break  # We can get out of the infinite loop
        newCoord = Coords(randint(0, range - 1), randint(0, range - 1))
    usedCoords.append(newCoord)
    return newCoord


def generateGameMap(mapSize):
    result = []
    result.append(["w" for x in range(mapSize)])
    poiCoords = {
        "f": [generateCoords(mapSize - 2), generateCoords(mapSize - 2)],
        "r": [generateCoords(mapSize - 2)] if randint(0, 1) == 1 else [None],
        "s": [generateCoords(mapSize - 2)],
        "v": [generateCoords(mapSize - 2)],
        "p": [generateCoords(mapSize - 2)],
    }
    for y in range(mapSize - 2):
        row = ["w"]
        for x in range(mapSize - 2):
            poiFound = False
            for r in poiCoords.keys():
                for loc in poiCoords[r]:
                    if loc == None:
                        continue
                    if loc.x == x and loc.y == y:
                        row.append(r)
                        poiFound = True
            if poiFound == False:
                row.append(" ")
        row.append("w")
        result.append(row)
    result.append(["w" for x in range(mapSize)])
    return result


@dataclass
class Event:
    story: str
    effect: str
    effectStrength: float


eventList = [
    Event("PLAYERNAME finds an inn and recovers some health", "HEL", 25),
    Event("PLAYERNAME trips over a log and loses some health", "HEL", -20),
    Event("PLAYERNAME finds a chest and opens it, and finds some gold!", "GOL", 1.5),
    Event(
        "PLAYERNAME sees an object on the floor and picks it up. Its a map!",
        "MAP",
        True,
    ),
]

# MAP INFO

symbolsOn = None


def formatMap(map):
    global symbolsOn
    result = []
    definition = {
        "w": "❌",
        "p": "🧑",
        " ": "  ",
        "s": "💰",
        "v": "❓",
        "f": "⚔️",
        "r": "🛏️",
    }
    for row in map:
        t = []
        for item in row:
            if symbolsOn:
                t.append(definition[item])
                continue
            t.append(item)
        result.append("".join(t))

    return "\n".join(result)


def displayMap(p, m):
    # if p.hasMap:
    print(formatMap(m))


# MOVEMENT


def handleMovement(
    m,
):  # returns an array containing the new map, and the new symbol stepped on
    global p

    newPosSymbol = "w"
    while newPosSymbol == "w":
        d, i = pick(["Up", "Down", "Right", "Left"], "Choose a direction to travel: ")
        # Match case not supported on repl yet
        for row in m:
            if "p" in row:
                playerPos = Coords(row.index("p"), m.index(row))
        newPos = (
            playerPos + basisDict[d]
        )  # We can add objects together by the class using __add__()
        newPosSymbol = m[newPos.y][newPos.x]
        if newPosSymbol == "w":
            os.system("clear")
            print("Invalid direction!")
            displayMap(p, m)
            _ = input("Press enter when ready to move: ")

    m[newPos.y][newPos.x] = "p"
    m[playerPos.y][playerPos.x] = " "
    return [m, newPosSymbol]


# GLOBALS

print(
    "Welcome to the game! Please use fullscreen or some text might be hidden! To test it, you should be able to read this whole sentence in one line without text wrapping round! Good luck!"
)
_ = input("Press enter when ready to start: ")
p = Player()
m = generateGameMap(5)
symbolsOn = (
    True
    if input("Do you want experimental map symbols on (often look bad)? (y/n) ").lower()
    == "y"
    else False
)

# TILE ACTIONS

# encounterList = [
#    Encounter(["Goblin", "Goblin"], 1, "Goblin Gang"),
#    Encounter(["Armoured Goblin"], 1, "Goblin Guard"),
# Encounter(["Armoured Goblin", "Striker Goblin"], 2, "Father and Son"),
# ]

# Fight sleep value (so can be adjusted easily)
fsv = 1


def fightFlow():
    global p
    e = getRandomEncounterOfLevel(p.currentFloor)
    print(f"You stumbled across a {e.id}!")
    print(f"Enemies: {', '.join(e.enemies)}")
    eList = [getEnemyDefinition(en) for en in e.enemies]
    while len(eList) > 0:
        # Player's turn
        os.system("clear")
        print("It's your turn!")
        time.sleep(fsv)
        edisplaylist = map(
            lambda enemy: f"{enemy.name}: . Health Remaining: {enemy.health}/{enemy.maxHealth}. Attack: {enemy.attack}"
        )
        n, i = pick(
            edisplaylist,
            f"Choose an enemy to attack!\nYour health remaining: {p.health}/{p.maxHealth}",
        )
        time.sleep(fsv)
        eHit = eList[i]
        if hasDodged(eHit) == False:
            dmg = randrange(
                (p.baseAttack + p.bonusAttack) - 3, (p.baseAttack + p.bonusAttack) + 3
            )
            eHit.health -= dmg
            if dmg == (p.baseAttack + p.bonusAttack) + 3:
                print("Critical hit!")
                time.sleep(fsv)
            print(
                f"You hit the {eHit.name} for {dmg} damage! It has {eHit.health}/{eList[i].maxHealth} remaining!"
            )
            time.sleep(fsv)
            if eHit.health <= 0:
                xp = randrange(
                    max(
                        0,
                        (eHit.xpGiven) - 10,
                        (eHit.baseAttack + eHit.bonusAttack) + 10,
                    )
                )
                gold = randrange(max(0, (eHit.goldGiven) - 1, (eHit.goldGiven) + 1))
                print(f"You killed the {eHit.name} and gained {xp} XP and {gold} Gold!")
                time.sleep(fsv)
                p.gainXP(xp)
                p.gainGold(gold)
                eList.remove(i)
        else:
            print(f"The {eHit.name} dodged your attack!")
            time.sleep(fsv)
        print('It\'s the enemies\' turn!')
        time.sleep(fsv)
        for e in eList:
          dmg = randrange(e.attack + 3, e.attack - 3)
          if (hasDodged(p) == False):
            print(f'{e.name} attacked for {dmg} damage!')
            if dmg == e.attack + 3:
              print('Critical hit!')
            p.takeDamage(dmg)
            print(f'Your health remaining: {p.health}/{p.maxHealth}')
            time.sleep(fsv)
    print('You have completed the battle. Congratulations!')


restDialogues = [
    "You found some shelter and healed for CONTENT health!",
    "You get a break from the action, healing CONTENT health!",
    "You find a quiet stream and decide to rest. You heal for CONTENT health!",
    "You find a cave and decide to stay the night. You heal CONTENT health!",
]


def restFlow():
    global p
    percentHealed = randrange(15, 30)
    healed = math.floor((percentHealed / 10) * p.maxHealth)
    p.changeHealth(healed)
    print(choice(restDialogues).replace("CONTENT", str(healed)))
    _ = input("Press enter to continue...")


def shopFlow():
    global p
    itemsInShop = [choice(items) for i in range(5)]
    rilist = list(
        map(
            lambda i: f"{i.name}: {i.description}. Duration: {i.duration} turns. Cost: {i.cost}",
            itemsInShop,
        )
    )  # readable item list
    rilist.append()
    rilist.append("Don't buy an item")
    # print(list(map(lambda i: f'{i.name}: {i.description}', p.inventory))) Some estoeric python which takes the array of current items and turns it into a more human readable format
    n, i = pick(
        rilist,
        f"Welcome to the shop!\nYou have {p.gold} gold.\nPick a SINGLE item to purchase.",
    )
    if (
        i != len(rilist) - 1
    ):  # If is the last item, the player chose "Don't use an item"
        goldCost = float(n.split(":")[-1].lstrip())
        if p.gold > goldCost:
            p.getItem(i)
            p.changeGold(p.gold - goldCost)
            print(f'{p.name} bought a {n.split(":")[0]}!')
        else:
            print("{p.name} didn't have enough money!")
    _ = input("Press enter when moving on: ")


def eventFlow():
    global p
    e = choice(eventList)
    p.addEffect(e.effect, e.effectStrength)
    print(e.story.replace("PLAYERNAME", p.name))
    i = "increased"
    d = "decreased"
    print(
        f"{p.name}'s {e.effect} was {i if e.effectStrength > 0 else d} by {e.effectStrength if e.effectStrength > 0 else -e.effectStrength}!"
    )


def exitFlow():
    global p
    print("You found the exit to floor {p.floor}!")
    xp = randrange(50, 150)
    print(f"You gained {xp} xp!")
    p.gainXP(xp)


tileDispatch = {
    " ": lambda _: _,
    "f": fightFlow,
    "r": restFlow,
    "s": shopFlow,
    "v": eventFlow,
    "e": exitFlow,
}


def processEvent(eventTile):
    global tileDispatch
    if eventTile == " ":
        return
    tileDispatch[eventTile]()


def useItemFlow():
    global p
    rilist = list(
        map(
            lambda i: f"{i.name}: {i.description}. Duration: {i.duration} turns",
            p.inventory,
        )
    )  # readable item list
    rilist.append("Don't use an item")
    # print(list(map(lambda i: f'{i.name}: {i.description}', p.inventory))) Some estoeric python which takes the array of current items and turns it into a more human readable format
    n, i = pick(rilist, "Choose an item from your inventory to use")
    if (
        i != len(rilist) - 1
    ):  # If is the last item, the player chose "Don't use an item"
        p.useItem(i)
        print(f'{p.name} used their {n.split(":")[0]}!')
    _ = input("Press enter when moving on: ")


def takeTurn():
    os.system("clear")
    global p, m
    d, i = pick(["No", "Yes"], "Do you want to use an Item? ")
    if i:
        useItemFlow()
    print(f"Current Floor: {p.currentFloor}")
    displayMap(p, m)
    _ = input("Press enter when ready to move (map will dissapear): ")
    d = handleMovement(m)
    os.system("clear")
    m = d[0]
    newTile = d[1]
    processEvent(newTile)
    p.itemQueueSweep()
    _ = input("End of turn! Press enter to continue: ")


####### GAME LOGIC #########
p.changeMapStatus(True)
p.findItem("Bulwark")

while True:
    takeTurn()
