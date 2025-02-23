import sys
import os
import pygame

ROOT_PATH = os.getenv("ROOT_PATH")
sys.path.append(ROOT_PATH)

from scripts.character import Character
from scripts.animation import Animation

class Blaze(Character):

  def __init__(self, x=0, y=0, max_y=260, min_y=10):
    self.name = "Rollerblader"
    self.speed = 5
    self.health = 100
    self.strength = 5
    self.agility = 10
    self.intelligence = 10
    self.charisma = 10
    self.size = 2
    animations = {
      "idle": Animation("./assets/sprites/blaze/idle.png", "./assets/animations/blaze/idle.json", use_velocity=False, loop=True),
      "walk": Animation("./assets/sprites/blaze/walk.png", "./assets/animations/blaze/walk.json", use_velocity=True, loop=True),
      "run": Animation("./assets/sprites/blaze/walk.png", "./assets/animations/blaze/run.json", use_velocity=True, loop=True),
    }
    super().__init__(x, y, width=self.size, height=self.size, animations=animations, use_gravity=False, min_y=min_y, max_y=max_y, speed=self.speed)

  def move(self, dx, dy):
      """Move o personagem no chão e permite movimentação limitada no eixo Y."""
      self.velocity_x = dx
      self.velocity_y = dy / 2  # 🔥 Mantém movimentação fluida

      screen_height = pygame.display.get_surface().get_height()
      current_y = screen_height - self.y - self.height / 2

      # 🔥 Só muda de animação quando aterrissa
      if not self.is_jumping:
          if self.velocity_x != 0 or self.velocity_y != 0:
              self.set_animation("run" if abs(self.velocity_x) > self.walk_speed else "walk")
          else:
              self.set_animation("idle")

      if not self.is_jumping:
          if current_y > self.min_y and dy > 0 or current_y < self.max_y and dy < 0:
              self.y += dy
          self.landing_y += dy

      if self.is_jumping:
          self.set_animation("jump")

      if dx != 0:
          if dx < 0:
              self.animation_handler.current_animation.set_flipped(False)
          elif dx > 0:
              self.animation_handler.current_animation.set_flipped(True)

  def update(self, params):
    super().update(params)

  def late_update(self, params):
    super().late_update(params)
  