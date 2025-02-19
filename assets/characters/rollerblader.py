import sys
import os

ROOT_PATH = os.getenv("ROOT_PATH")
sys.path.append(ROOT_PATH)

from scripts.character import Character
from scripts.animation import Animation

class Rollerblader(Character):

  def __init__(self, x=0, y=0):
    self.name = "Rollerblader"
    self.speed = 10
    self.health = 100
    self.strength = 5
    self.agility = 10
    self.intelligence = 5
    self.charisma = 10
    self.height = 100
    self.width = 50
    animations = {
      "idle": Animation("./assets/sprites/rollerblader/idle.png", "./assets/animations/rollerblader/idle.json", use_velocity=True, loop=True),
      "walk": Animation("./assets/sprites/rollerblader/walk.png", "./assets/animations/rollerblader/walk.json", use_velocity=True, loop=True),
      "run": Animation("./assets/sprites/rollerblader/run.png", "./assets/animations/rollerblader/run.json", use_velocity=True, loop=True),
      "jump": Animation("./assets/sprites/rollerblader/jump.png", "./assets/animations/rollerblader/jump.json", use_velocity=True),
      "dodge": Animation("./assets/sprites/rollerblader/dodge.png", "./assets/animations/rollerblader/dodge.json", use_velocity=True),
      "fall": Animation("./assets/sprites/rollerblader/fall.png", "./assets/animations/rollerblader/fall.json", use_velocity=True, loop=True),
    }
    super().__init__(x, y, width=self.width, height=self.height, animations=animations, use_gravity=True)

  def update(self, params):
    super().update(params)
  