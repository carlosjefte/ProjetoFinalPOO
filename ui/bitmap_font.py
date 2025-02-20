import json
import pygame
import sys
import os

class BitmapFont:
    def __init__(self, image_path, json_path):
        """Inicializa a fonte bitmap carregando a imagem e o mapeamento de caracteres."""
        self.image = pygame.image.load(image_path).convert_alpha()

        with open(json_path, "r", encoding="utf-8") as file:
            char_data = json.load(file)

        # Criar um dicionário para acesso rápido aos caracteres
        self.char_map = {data["name"]: (data["x"], data["y"], data["width"], data["height"]) for data in char_data}

        char_list = """ !"',-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"""

    def render(self, text, color=(255, 255, 255), font_size=16):
        """Gera uma superfície com o texto renderizado corretamente e escalado."""
        if not text:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        scale_factor = font_size / 16  # Como a fonte base tem 16x16, usamos essa proporção
        char_spacing = int(2 * scale_factor)
        num_spaces = text.count(" ")

        width = sum(int(self.char_map.get(char, (0, 0, 0, 0))[2] * scale_factor) for char in text if char in self.char_map)  
        width += (len(text) - 1) * char_spacing
        width += int((num_spaces * 2) * (scale_factor * char_spacing)) # Pequeno buffer extra para evitar corte
        height = max((int(self.char_map.get(char, (0, 0, 0, 0))[3] * scale_factor) for char in text if char in self.char_map), default=1)

        text_surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        text_surface.fill((0, 0, 0, 0))

        x_offset = 0
        for char in text:
            if char in self.char_map:
                char_x, char_y, char_w, char_h = self.char_map[char]
                char_rect = pygame.Rect(char_x, char_y, char_w, char_h)
                char_image = self.image.subsurface(char_rect)
                char_image = pygame.transform.scale(char_image, (int(char_w * scale_factor), int(char_h * scale_factor)))

                # Ajuste de cor sem alterar a opacidade
                char_image.fill(color, special_flags=pygame.BLEND_RGBA_MIN)

                text_surface.blit(char_image, (x_offset, 0))
                x_offset += char_image.get_width() + char_spacing
            elif char == " ":
                space_width = int(8 * scale_factor)  # Ajustável conforme necessário
                x_offset += space_width + char_spacing

        return text_surface


if __name__ == "__main__":
    pygame.init()

    ROOT_PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
    font_png = os.path.join(ROOT_PATH, "assets", "fonts", "title-font.png")
    font_json = os.path.join(ROOT_PATH, "assets", "fonts", "title-font-positions.json")

    screen = pygame.display.set_mode((800, 200))
    pygame.display.set_caption("Teste de Fonte")

    font = BitmapFont(font_png, font_json)

    test_text = "HELLO WORLD"
    rendered_text = font.render(test_text, font_size=32)  # Ajuste o tamanho da fonte

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(rendered_text, (50, 50))
        pygame.display.flip()

    pygame.quit()