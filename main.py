from random import randrange, randint
import shutil # Finding terminal size, for centering
from dataclasses import dataclass
from typing import Any
from pick import pick

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

def getEnemyDefinition(enemyName):
  global enemies
  for enemy in enemies:
    if enemy.name == enemyName:
      return enemy
  raise KeyError(f'No enemy with name "{enemyName}"')

# Handling rankups
rankOrder = [ROOKIE, NOVICE, CADET, ADEPT, MASTER, LEGEND, OVERLORD]
class Player:
  def __init__(self):
    self.name = input('Enter your player\'s name: ')
    self.health: int = 100
    self.maxHealth: int = 100
    self.dodge: int = 2 # Base dodge is 2%
    self.essence: float = 0
    self.rank = ROOKIE
    self.xpToNextRank = rankOrder[rankOrder.index(self.rank)].xpRequired
    self.baseAttack = self.rank.baseAttack
    self.bonusAttack = 0
    self.inventory = []
    self.kills = 0
    self.currentFloor = 1
    self.itemQueue = []

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

  def changeEssence(self, newEssence):
    self.essence = newEssence

  def changeBonusAttack(self, newBonusAttack):
    self.bonusAttack = newBonusAttack

  def addKill(self):
    self.kills += 1

  def addFloor(self):
    self.currentFloor += 1

  # THIS IS WHERE ITEM EFFECTS ARE DEFINED
  dispatch = {'NAM':changeName, 'HEL':changeHealth, 'MAX':changeMaxHealth, 'DOD':changeDodge}  
  
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

class Enemy:
  def __init__(self, enemyName, enemyAttack, enemyHP, dodge):
    self.name = enemyName
    self.attack = enemyAttack
    self.health = enemyHP
    self.dodge = dodge
  

def hasDodged(e) -> bool: # e -> entity
  # We need to refer to the global variable of the player
  # Generates a random integer between 0 and 100 inclusive
  dodgeValue = randrange(101)
  # The greater the player dodge, the more likely that this evaluates to true
  # We can just return the expression as it will evaluate to true or false itself
  return dodgeValue <= e.dodge

@dataclass
class Coords:
  x: int
  y: int

usedCoords = []
# We need to ensure that duplicate coords are not present, naive approach so I'll have a look later
def generateCoords(range):
  global usedCoords
  valid = True
  newCoord = Coords(randint(0, range - 1), randint(0, range - 1))
  while True:
    for item in usedCoords:
      if item.x == newCoord.x and item.y == newCoord.y:
        valid = False
    if valid:
      break # We can get out of the infinite loop
    newCoord = Coords(randint(0, range - 1), randint(0, range - 1))
  return newCoord
  
def generateGameMap(mapSize):
  result = []
  result.append(['w' for x in range(mapSize)])
  poiCoords = {'f':generateCoords(mapSize - 2), 'r':generateCoords(mapSize - 2) if randint(0, 1) == 1 else Coords(0,0), 's':generateCoords(mapSize - 2), 'v':generateCoords(mapSize - 2)} 
  for y in range(mapSize - 2):
    row = ['w']
    for x in range(mapSize - 2):
      poiFound = False
      for poi in poiCoords.keys():
        if poiCoords[poi].x == x and poiCoords[poi].y == y:
          row.append(poi)
          poiFound = True
      if poiFound == False:
        row.append('')
    row.append('w')
    result.append(row)
  result.append(['w' for x in range(mapSize)])
  return result
    
####### GAME LOGIC #########

print(generateGameMap(5))
