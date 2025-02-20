import os
import pygame
from ui.bitmap_font import BitmapFont

ROOT_PATH = os.environ["ROOT_PATH"]
FONT_PATH = os.path.join(ROOT_PATH, "assets", "fonts", "title-font.png")
JSON_PATH = os.path.join(ROOT_PATH, "assets", "fonts", "title-font-positions.json")

pygame.init()  # Inicializa o pygame para evitar erros ao carregar a imagem

bitmap_font = BitmapFont(FONT_PATH, JSON_PATH)  # Instância global da fonte