from random import randrange

class Rank:
  def __init__(self, name, xpRequired, baseHP, baseAttack, baseDodge):
    self.name = name
    self.baseHP = baseHP
    self.baseAttack = baseAttack
    self.baseDodge = baseDodge
    self.xpRequired = xpRequired

# Ranks
ROOKIE = Rank('ROOKIE', 0, 100, 20, 2)
NOVICE = Rank('NOVICE', 200, 120, 25, 4)
CADET = Rank('CADET', 300, 145, 33, 6)
ADEPT = Rank('ADEPT', 500, 175, 41, 8)
MASTER = Rank('MASTER', 700, 210, 50, 10)
LEGEND = Rank('LEGEND', 800, 250, 60, 12)
OVERLORD = Rank('OVERLORD', 1000, 325, 75, 15)

# Handling rankups
rankOrder = [ROOKIE, NOVICE, CADET, ADEPT, MASTER, LEGEND, OVERLORD]

class Player:
  def __init__(self, playerName):
    global rankOrder
    self.name = playerName
    self.health: int = 100
    self.maxHealth: int = 100
    self.dodge: int = 2 # Base dodge is 2%
    self.ACG: float = 0
    self.rank = ROOKIE
    self.xpToNextRank = rankOrder[rankOrder.index(self.rank) + 1].xpRequired
    self.attack = self.rank.baseAttack
    self.inventory = []
    self.kills = 0
    self.currentFloor = 1
    
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

