from random import randrange

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

# Handling rankups
rankOrder = [ROOKIE, NOVICE, CADET, ADEPT, MASTER, LEGEND, OVERLORD]


class Player:
  def __init__(self, playerName):
    self.name = playerName
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
    self.effectQueue = []


  def changeHealth(self, newHealth):
    self.health = newHealth
    # Check if dies?

  def changeName(self, newName):
    self.name = newName

  def changeMaxHealth(self, newMaxHealth):
    self.maxHealth = newMaxHealth

  def changeDodge(self, newDodge):
    self.dodge = newDodge

  def changeEssence(self, newEssence):
    self.essence = newEssence

  def rankUp(self):
    self.rank = rankOrder[rankOrder.index(self.rank) + 1]

  def changeBonusAttack(self, newBonusAttack):
    self.bonusAttack = newBonusAttack

  def addKill(self):
    self.kills += 1

  def addFloor(self):
    self.currentFloor += 1
  
  dispatch = {'NAM':changeName, 'HEL':changeHealth, 'MAX':changeMaxHealth}  
  
  def addEffect(self, effectCode, value):
    self.dispatch[effectCode](self, value)
    print(f'Added effect {effectCode} with value {value}')

  
  
  
  
  
    
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
p = Player('Rowan')
print(p.name)
print(p.health)
p.addEffect('HEL', 50)
print(p.health)