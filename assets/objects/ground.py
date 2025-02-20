import sys
import os

sys.path.append(os.getenv("ROOT_PATH"))
ROOT_PATH = os.getenv("ROOT_PATH")
from scripts.objects import Object
from scripts.animation import Animation

class Ground(Object):
    """Representa o chão da cena."""
    def __init__(self, x, y, width, height):
        animations = {
            # Utilizes ROOT_PATH to get animation path
            "idle": Animation(os.path.join(ROOT_PATH, "assets", "textures", "ground.png"), os.path.join(ROOT_PATH, "assets", "animations", "textures", "city_background.json"))
        }
        super().__init__(x, y, animations, width, height, use_gravity=False, use_collision=True)