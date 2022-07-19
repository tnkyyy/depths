from random import randrange, randint, choice
import shutil # Finding terminal size, for centering
from dataclasses import dataclass
from typing import Any
from pick import pick
import os

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
ROOKIE = Rank('ROOKIE', 200, 100, 20, 2)
NOVICE = Rank('NOVICE', 300, 120, 25, 4)
CADET = Rank('CADET', 500, 145, 33, 6)
ADEPT = Rank('ADEPT', 700, 175, 41, 8)
MASTER = Rank('MASTER', 800, 210, 50, 10)
LEGEND = Rank('LEGEND', 1000, 250, 60, 12)
OVERLORD = Rank('OVERLORD', 9999, 325, 75, 15)

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
items = [Item('Bulwark', 'Adds maximum health to bolster defence', 3, False, 'MAX', None, 50, None, 2.50),
         Item('Stim', 'Increases your dodge significantly but reduces your maximum health.', 2, False, 'DOD', 'MAX', 20, -25, 4),
        Item('Name Tag', 'Allows you to change your name', 0, True, 'NAM', None, 1, 1, 3)]

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
    self.name = input('Enter your player\'s name: ')
    self.health: int = 100
    self.maxHealth: int = 100
    self.dodge: int = 2 # Base dodge is 2%
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

  def rankUp(self):
    self.rank = rankOrder[rankOrder.index(self.rank) + 1]
    self.xpToNextRank = rankOrder[rankOrder.index(self.rank)].xpRequired
    print(f'\n{self.name} ranked up to {self.rank.name}! XP Required for next rank: {self.xpToNextRank}\n')
  
  def changeHealth(self, newHealth):
    self.health = newHealth
    # Check if dies?

  def changeName(self, defaultParameter):
    newName = ''
    while newName == '':
      newName = input('Enter a new name for your character: ')

  def changeMaxHealth(self, newMaxHealth):
    self.maxHealth += newMaxHealth

  def changeDodge(self, newDodge):
    self.dodge += newDodge

  def changeGold(self, newGold):
    self.gold = newGold

  def changeBonusAttack(self, newBonusAttack):
    self.bonusAttack = newBonusAttack

  def findItem(self, itemCode):
    global getItemDefinition
    self.getItem(getItemDefinition(itemCode))

  def changeMapStatus(self, hasMap):
    self.hasMap = hasMap
    
  # THIS IS WHERE ITEM EFFECTS ARE DEFINED
  dispatch = {'NAM':changeName, 'HEL':changeHealth, 'MAX':changeMaxHealth, 'DOD':changeDodge, 'GOL':changeGold, 'BOA':changeBonusAttack, 'MAP':changeMapStatus}  

  def addKill(self):
    self.kills += 1

  def addFloor(self):
    self.currentFloor += 1
  
  def addEffect(self, effectCode, value):
    self.dispatch[effectCode](self, value)

  def removeEffect(self, effectCode, value):
    self.dispatch[effectCode](self, -value)

  def useItem(self, itemIndex):
    item = self.inventory.pop(itemIndex)
    self.addEffect(item.effect, item.strength)
    if item.secondaryEffect != None:
      self.addEffect(item.secondaryEffect, item.secondaryStrength)
    if item.isOneOff == False:
      self.itemQueue.append(ItemQueueEntry(item.name, item.duration, item.effect, item.secondaryEffect, item.strength, item.secondaryStrength))
  
  def itemQueueSweep(self):
    for item in self.itemQueue:
      if item.turnsTillExpiration == 1:
        if item.secondaryEffectCode != None:
          self.removeEffect(item.secondaryEffectCode, item.secondaryEffectStrength)
        self.removeEffect(item.effectCode, item.effectStrength)
        print(f'{self.name}\'s {item.itemName} expired!')
        self.itemQueue.pop(self.itemQueue.index(item))
      else:
        item.turnsTillExpiration -= 1

  def getItem(self, item):
    self.inventory.append(item)

  def newTurn(self):
    self.itemQueueSweep()

  def getItemIndexFromPrompt(self):
    promptArr = []
    returnPrompt = '--- Return ---'
    title = 'Choose an item to use: '
    for item in self.inventory:
      promptArr.append(f'{item.name}: {item.description}')
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

  def newFloor(self):
    self.addFloor()
    self.removeMap()


class Enemy:
  def __init__(self, enemyName, enemyAttack, enemyHP, dodge, xpGiven, goldGiven):
    self.name = enemyName
    self.attack = enemyAttack
    self.health = enemyHP
    self.dodge = dodge
    self.xpGiven = xpGiven
    self.goldGiven = goldGiven

  def takeDamage(self, damage):
    self.health -= damage

enemyList = [
  Enemy('Goblin', 5, 30, 1, 15, 0.1),
  Enemy('Armoured Goblin', 3, 50, 0, 25, 0.2),
  Enemy('Striker Goblin', 7, 20, 10, 10, 0.1)
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
  Encounter([
    'Goblin','Goblin'
  ], 1, 'Goblin Gang'),
  Encounter([
    'Armoured Goblin'
  ], 1, 'Goblin Guard'),
  Encounter([
    'Armoured Goblin', 'Striker Goblin'
  ], 2, 'Father and Son')
]

def getRandomEncounterOfLevel(minLevel):
  e = choice(encounterList)
  while e.minLevel > minLevel:
    e = choice(encounterList)

  return e



def hasDodged(e) -> bool: # e -> entity
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

  def __add__(c1, c2): # So we can add coordinates together for handling movement
    return Coords(c1.x + c2.x, c1.y + c2.y)

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
      break # We can get out of the infinite loop
    newCoord = Coords(randint(0, range - 1), randint(0, range - 1))
  usedCoords.append(newCoord)
  return newCoord
  
def generateGameMap(mapSize):
  result = []
  result.append(['w' for x in range(mapSize)])
  poiCoords = {'f':generateCoords(mapSize - 2), 'r':generateCoords(mapSize - 2) if randint(0, 1) == 1 else None, 's':generateCoords(mapSize - 2), 'v':generateCoords(mapSize - 2), 'p':generateCoords(mapSize - 2)} 
  for y in range(mapSize - 2):
    row = ['w']
    for x in range(mapSize - 2):
      poiFound = False
      for poi in poiCoords.keys():
        if poiCoords[poi] == None:
          continue
        if poiCoords[poi].x == x and poiCoords[poi].y == y:
          row.append(poi)
          poiFound = True
      if poiFound == False:
        row.append(' ')
    row.append('w')
    result.append(row)
  result.append(['w' for x in range(mapSize)])
  return result

@dataclass
class Event:
  story: str
  effect: str
  effectStrength: float

events = [
  Event('PLAYERNAME finds an inn and recovers some health',
       'HEL',
       25),
  Event('PLAYERNAME trips over a log and loses some health',
       'HEL',
       -20),
  Event('PLAYERNAME finds a chest and opens it, and finds some gold!',
       'GOL',
       1.5),
  Event('PLAYERNAME sees an object on the floor and picks it up. Its a map!',
       'MAP',
       True)
]

symbolsOn = None

def formatMap(map):
  global symbolsOn
  result = []
  definition = {'w':'█', 'p':'🧍', ' ':' ', 's':'💰', 'v':'❓', 'f':'⚔', 'r':'🛏'}
  for row in map:
    t = []
    for item in row:
      if symbolsOn:
        t.append(definition[item])
        continue
      t.append(item)
    result.append(''.join(t))

  return '\n'.join(result)

def displayMap(p, m):
  if p.hasMap:
    print(formatMap(m))

def handleMovement(m):
  basisDict = {'Up':Coords(0, -1), 'Down':Coords(0, 1), 'Right':Coords(1, 0), 'Left':Coords(-1, 0)}
  d, i = pick(['Up', 'Down', 'Right', 'Left'], 'Choose a direction to travel: ')
  # Match case not supported on repl yet
  for row in map:
    if 'p' in row:
      playerPos = Coords(row.index('p'), map.index(row))
  newPos = playerPos + basisDict[d] # We can add objects together by the class using __add__()
  
  



p = Player()
m = generateGameMap(5)
symbolsOn = True if input('Do you want experimental map symbols on (often look bad)? (y/n) ') == 'y' else False

def takeTurn():
  os.system('clear')
  global p, m
  displayMap(p, m)
  x = input('Press enter when ready to move: ')
####### GAME LOGIC #########


handleMovement(m)