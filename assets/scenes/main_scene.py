import pygame
from random import randint, uniform
import sys
import os
from assets.objects.jeep import Jeep  # Import the Jeep class

sys.path.append(os.getenv("ROOT_PATH"))
from scripts.game_scene import GameScene
from assets.objects.ground import Ground
from assets.characters.rollerblader import Rollerblader

class MainScene(GameScene):
    """Cena principal do jogo com chão, personagem e jipes."""
    def __init__(self, screen):
        super().__init__(screen)

        # Criando o chão
        self.ground_y = 700  # Define a posição correta do chão
        self.max_y = 700
        self.min_y = 10

        # Carregando os backgrounds
        root_path = os.getenv("ROOT_PATH")
        self.main_backgrounds = [
            self.load_and_scale_background(os.path.join(root_path, "assets", "sprites", "street", "background-1.png"))
            # self.load_and_scale_background(os.path.join(root_path, "assets", "sprites", "street", "background-2.png"))
        ]
        self.background = [{"image": self.main_backgrounds[0], "x": 0, "y": 0}]

        self.bg_width = self.main_backgrounds[0].get_width()  # Pegamos a largura do primeiro fundo

        for bg in self.main_backgrounds:
            print(bg.get_width(), bg.get_height())  # Isso imprime o tamanho de cada fundo

        self.player = None

        # Jeep spawning logic
        self.jeeps = []  # Lista de jipes ativos
        self.last_spawn_time = 0  # Tempo do último spawn
        self.spawn_interval = randint(2, 5)  # Intervalo inicial entre spawns (em segundos)

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
        """Atualiza a cena, personagem e spawn de jipes."""
        if params["selected_character"] is None and self.player is None:
            self.player = Rollerblader()
            player_x = 300
            player_y = self.ground_y - self.player.height  # Usa a altura do personagem
            params["main_update"]({"selected_character": self.player})
            print(f"🎮 Adicionando personagem na posição ({player_x}, {player_y})")
            self.player.set_position(player_x, player_y)
            self.add_object(self.player)
        if params["selected_character"] and self.player is None:
            self.player = params["selected_character"]
            player_x = 300
            player_y = self.ground_y - self.player.height  # Usa a altura do personagem
            print(f"🎮 Adicionando personagem na posição ({player_x}, {player_y})")
            self.player.set_position(player_x, player_y)
            self.add_object(self.player)

        # Atualiza o spawn de jipes
        # self.spawn_jeeps(params.get("dt", 0))

        # Atualiza todos os jipes ativos
        for jeep in self.jeeps:
            jeep.update(params)

        super().update(params)

    def spawn_jeeps(self, dt):
        """Lógica para spawnar jipes fora da visão do jogador."""
        self.last_spawn_time += dt

        # Verifica se é hora de spawnar um novo jipe
        if self.last_spawn_time >= self.spawn_interval:
            self.last_spawn_time = 0  # Reseta o contador
            self.spawn_interval = randint(2, 5)  # Define um novo intervalo aleatório

            # Escolhe um lado aleatório para spawnar o jipe (esquerda ou direita)
            spawn_side = randint(0, 1)  # 0 = esquerda, 1 = direita
            screen_width, _ = self.screen.get_size()

            # Define a posição inicial do jipe
            if spawn_side == 0:
                x = -100  # Fora da tela à esquerda
                velocity_x = uniform(2, 5)  # Velocidade positiva (movendo para a direita)
            else:
                x = screen_width + 100  # Fora da tela à direita
                velocity_x = uniform(-5, -2)  # Velocidade negativa (movendo para a esquerda)

            # Cria o jipe
            jeep = Jeep(x, self.ground_y - 50)  # Ajusta a posição Y para o chão
            jeep.velocity_x = velocity_x  # Define a velocidade
            self.jeeps.append(jeep)
            self.add_object(jeep)

    def update_background(self):
        """Aplica parallax no fundo e adiciona/remove fundos conforme necessário."""
        screen_width, _ = self.screen.get_size()  # Obtém dinamicamente a largura da tela

        if self.player is not None and self.player.velocity_x != 0:
            for bg in self.background:
                bg["x"] -= self.player.velocity_x

            direction = 1 if self.player.velocity_x > 0 else -1

            # 🔥 Adiciona um novo fundo na borda direita ou esquerda conforme a direção do movimento
            if direction > 0:  # Indo para a direita
                if self.background[-1]["x"] + self.bg_width <= screen_width + 20:
                    new_bg = {
                        "image": self.main_backgrounds[randint(0, len(self.main_backgrounds) - 1)],
                        "x": self.background[-1]["x"] + self.bg_width,
                        "y": 0
                    }
                    self.background.append(new_bg)

            else:  # Indo para a esquerda
                if self.background[0]["x"] >= -20:
                    new_bg = {
                        "image": self.main_backgrounds[randint(0, len(self.main_backgrounds) - 1)],
                        "x": self.background[0]["x"] - self.bg_width,
                        "y": 0
                    }
                    self.background.insert(0, new_bg)  # 🔥 Adiciona na frente da lista

            # 🔥 Remove o fundo que sai completamente da tela
            if self.background[0]["x"] + self.bg_width < -50:  # Fundo da esquerda
                self.background.pop(0)
            elif self.background[-1]["x"] > screen_width + 50:  # Fundo da direita
                self.background.pop(-1)

    def draw(self):
        """Desenha a cena com o fundo, chão, personagem e jipes."""
        for bg in self.background:
            self.screen.blit(bg["image"], (bg["x"], bg["y"]))

    def late_update(self, params):
        """Método opcional chamado após o update()."""
        self.update_background()
        self.draw()
        super().late_update(params)