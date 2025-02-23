import sys
import os

ROOT_PATH = os.getenv("ROOT_PATH")
sys.path.append(ROOT_PATH)

from scripts.character import Character
from scripts.animation import Animation

class Rollerblader(Character):

  def __init__(self, x=0, y=0, max_y=260, min_y=10):
    self.name = "Rollerblader"
    self.speed = 7
    self.health = 100
    self.strength = 5
    self.agility = 10
    self.intelligence = 5
    self.charisma = 10
    self.size = 2.2
    animations = {
      "idle": Animation("./assets/sprites/rollerblader/idle.png", "./assets/animations/rollerblader/idle.json", use_velocity=False, loop=True),
      "walk": Animation("./assets/sprites/rollerblader/walk.png", "./assets/animations/rollerblader/walk.json", use_velocity=True, loop=True),
      "run": Animation("./assets/sprites/rollerblader/run.png", "./assets/animations/rollerblader/run.json", use_velocity=True, loop=True),
      "jump": Animation("./assets/sprites/rollerblader/jump.png", "./assets/animations/rollerblader/jump.json", use_velocity=False),
      "dodge": Animation("./assets/sprites/rollerblader/dodge.png", "./assets/animations/rollerblader/dodge.json", use_velocity=False),
      "fall": Animation("./assets/sprites/rollerblader/fall.png", "./assets/animations/rollerblader/fall.json", use_velocity=True, loop=True),
    }
    super().__init__(x, y, width=self.size, height=self.size, animations=animations, use_gravity=False, min_y=min_y, max_y=max_y, speed=self.speed)

  def update(self, params):
    super().update(params)

  def late_update(self, params):
    super().late_update(params)
  