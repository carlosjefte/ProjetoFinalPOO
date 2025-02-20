import pygame
from random import randint
import sys
import os

sys.path.append(os.getenv("ROOT_PATH"))
from scripts.game_scene import GameScene
from assets.objects.ground import Ground

class MainScene(GameScene):
    """Cena principal do jogo com chão e personagem."""
    def __init__(self, screen):
        super().__init__(screen)

        # Criando o chão
        self.ground_y = 600  # Define a posição correta do chão
        self.ground = Ground(0, self.ground_y, 1280, 50)
        self.add_object(self.ground)

        # Carregando os backgrounds
        root_path = os.getenv("ROOT_PATH")
        self.main_backgrounds = [
            self.load_and_scale_background(os.path.join(root_path, "assets", "sprites", "street", "background-1.png")),
            self.load_and_scale_background(os.path.join(root_path, "assets", "sprites", "street", "background-2.png"))
        ]
        self.background = [{"image": self.main_backgrounds[0], "x": 0, "y": 0}]

        self.bg_width = self.main_backgrounds[0].get_width()  # Pegamos a largura do primeiro fundo

        for bg in self.main_backgrounds:
            print(bg.get_width(), bg.get_height())  # Isso imprime o tamanho de cada fundo

        self.player = None

    def load_and_scale_background(self, image_path):
        """Carrega e reescala o background para que sua altura preencha a tela sem deformação."""
        screen_width, screen_height = self.screen.get_size()
        original_image = pygame.image.load(image_path)

        # Obtém dimensões originais
        original_width, original_height = original_image.get_size()

        # Calcula o fator de escala baseado na altura
        scale_factor = screen_height / original_height

        # Nova largura ajustada proporcionalmente
        new_width = int(original_width * scale_factor)
        new_height = screen_height  # Garante que a altura seja exata

        # Redimensiona mantendo a proporção
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
        
        return scaled_image

    def update(self, params):
        """Atualiza a cena e impede o personagem de atravessar o chão."""
        if params.get("selected_character") and self.player is None:
            self.player = params["selected_character"]
            player_x = 300
            player_y = self.ground_y - self.player.height  # Usa a altura do personagem
            self.player.set_position(player_x, player_y)
            self.add_object(self.player)

        self.update_background()
        super().update(params)

    def update_background(self):
        """Aplica parallax no fundo e adiciona/remova fundos conforme necessário."""
        screen_width, _ = self.screen.get_size()  # Obtém dinamicamente a largura da tela

        for bg in self.background:
            bg["x"] -= 2  # Move o fundo para a esquerda

        # Adiciona um novo fundo um pouco antes da borda da tela
        if self.background[-1]["x"] + self.bg_width <= screen_width + 20:
            new_bg = {
                "image": self.main_backgrounds[randint(0, 1)],
                "x": self.background[-1]["x"] + self.bg_width,
                "y": 0
            }
            self.background.append(new_bg)

        # Remove o primeiro fundo somente quando ele estiver totalmente fora
        if self.background[0]["x"] + self.bg_width < -50:
            self.background.pop(0)

    def draw(self):
        """Desenha a cena com o fundo, chão e personagem."""
        for bg in self.background:
            self.screen.blit(bg["image"], (bg["x"], bg["y"]))

    def late_update(self, params):
        """Método opcional chamado após o update()."""
        self.draw()