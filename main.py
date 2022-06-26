from random import randrange
import shutil # Finding terminal size, for centering
from dataclasses import dataclass
from typing import Any

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

  def changeName(self, newName):
    self.name = newName

  def changeMaxHealth(self, newMaxHealth):
    self.maxHealth += newMaxHealth

  def changeDodge(self, newDodge):
    self.dodge = newDodge

  def changeEssence(self, newEssence):
    self.essence = newEssence

  def changeBonusAttack(self, newBonusAttack):
    self.bonusAttack = newBonusAttack

  def addKill(self):
    self.kills += 1

  def addFloor(self):
    self.currentFloor += 1

  # THIS IS WHERE ITEM EFFECTS ARE DEFINED
  dispatch = {'NAM':changeName, 'HEL':changeHealth, 'MAX':changeMaxHealth}  
  
  def addEffect(self, effectCode, value):
    self.dispatch[effectCode](self, value)

  def removeEffect(self, effectCode, value):
    self.dispatch[effectCode](self, -value)

  def useItem(self, itemIndex):
    item = self.inventory.pop(itemIndex)
    self.addEffect(item.effect, item.strength)
    if item.secondaryEffect != None:
      self.addEffect(item.secondaryEffect, item.secondaryStrength)
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
        
@dataclass
class Item:
  name: str
  description: str
  duration: int
  effect: str
  secondaryEffect: Any
  strength: int
  secondaryStrength: Any
  cost: float

# This will be moved to a different file later
i_bulwark = Item('Bulwark', 'Adds maximum health to bolster defence', 3, 'MAX', None, 50, None, 2.50)

class Enemy:
  def __init__(self, enemyName, enemyAttack, enemyHP):
    self.name = enemyName
    self.attack = enemyAttack
    self.health = enemyHP
  

def hasDodged() -> bool:
  # We need to refer to the global variable of the player
  global mainPlayer
  # Generates a random integer between 0 and 100 inclusive
  dodgeValue = randrange(101)
  # The greater the player dodge, the more likely that this evaluates to true
  # We can just return the expression as it will evaluate to true or false itself
  return dodgeValue <= mainPlayer.dodge



# Game Logic
p = Player()
print(p.maxHealth)
p.getItem(i_bulwark)
print(p.maxHealth)
p.useItem(0)
print(p.maxHealth)
p.newTurn()
print(p.maxHealth)
p.newTurn()
print(p.maxHealth)
p.newTurn()
print(p.maxHealth)
p.newTurn()
print(p.maxHealth)
